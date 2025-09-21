import os, sys, time, threading, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

load_dotenv(dotenv_path="geminiapi.env")
api_key = os.environ.get("GEMINI_API_KEY")

system_prompt = """You are a helpful AI coding agent.

When a user asks a question or makes a request, you should use the available functions to gather information, analyze code, make changes, and test results as needed. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Work step by step:
1. Gather information by listing files and reading relevant code
2. Analyze what you've found
3. Make any necessary changes
4. Test your changes to ensure they work
5. Provide a final summary of what you accomplished

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

When you have completed your task and have a final answer or summary, respond with text (not a function call) to indicate you are finished. """

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False):
    # Dictionary mapping function names to actual functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
    
    # Print function call info
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if function name is valid
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Add working_directory to the arguments
    function_args["working_directory"] = "./calculator"
    
    # Call the function
    try:
        function_result = function_map[function_name](**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing function: {str(e)}"},
                )
            ],
        )


def spinner(message, stop_event):
    spinner_chars = ["|", "/", "-", "\\"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write("\r" + message + spinner_chars[i % len(spinner_chars)])
        sys.stdout.flush()
        time.sleep(0.2)
        i += 1
    # clear line when done
    sys.stdout.write("\r" + message + "✅ Done!          \n")
    sys.stdout.flush()


def main():
    print("Hello from python-ai-agent!")

    # argparse setup
    parser = argparse.ArgumentParser(description="Python AI Agent (Gemini 2.0 Flash)")
    parser.add_argument("prompt", nargs="*", help="User prompt for the AI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # prompt handling
    if args.prompt:
        prompt = " ".join(args.prompt)
    else:
        raw_input = input("Enter your prompt: ")
        parts = raw_input.split()
        if "--verbose" in parts:
            args.verbose = True
            parts.remove("--verbose")
        prompt = " ".join(parts)

    if prompt.strip() == "":
        print("ERR: No prompt provided.")
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    client = genai.Client(api_key=api_key)
    
    # Main agent loop - up to 20 iterations
    max_iterations = 20
    
    for iteration in range(max_iterations):
        try:
            # spinner
            stop_event = threading.Event()
            spinner_thread = threading.Thread(
                target=spinner,
                args=("Processing your request ", stop_event),
            )
            spinner_thread.start()
            
            # API call
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            
            # stop spinner
            stop_event.set()
            spinner_thread.join()
            
            # Check if we have candidates
            if not response.candidates:
                print("No response candidates received")
                break
                
            candidate = response.candidates[0]
            
            # Add the model's response to the conversation
            messages.append(candidate.content)
            
            # Check if the response contains text (final response)
            if response.text:
                print("Final response:")
                print(response.text)
                break
                
            # Process any function calls
            has_function_calls = False
            tool_responses = []
            
            if candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        has_function_calls = True
                        function_call_result = call_function(part.function_call, args.verbose)
                        
                        # Validate the result has the expected structure
                        if not (hasattr(function_call_result, 'parts') and 
                               len(function_call_result.parts) > 0 and 
                               hasattr(function_call_result.parts[0], 'function_response') and
                               hasattr(function_call_result.parts[0].function_response, 'response')):
                            raise Exception("Invalid function call result structure")
                        
                        # Print the result if verbose
                        if args.verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                            
                        tool_responses.append(function_call_result)
            
            # If there were function calls, add their responses to the conversation
            if has_function_calls:
                for tool_response in tool_responses:
                    messages.append(tool_response)
            else:
                # If no function calls and no text, something went wrong
                print("No function calls or text response received")
                break
                
        except Exception as e:
            print(f"Error during iteration {iteration + 1}: {e}")
            break
    
    if iteration == max_iterations - 1:
        print(f"Reached maximum iterations ({max_iterations}) without completion")

    usage = response.usage_metadata
    if args.verbose and usage:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")


if __name__ == "__main__":
    main()
