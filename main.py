import os, sys, time, threading, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv(dotenv_path="geminiapi.env")
api_key = os.environ.get("GEMINI_API_KEY")

verbose = False
if "--verbose" in sys.argv:
    verbose = True
    sys.argv.remove("--verbose")

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
    
    parser = argparse.ArgumentParser(description="Python AI Agent (Gemini 2.0 Flash)")
    parser.add_argument("prompt", nargs="*", help="User prompt for the AI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

       
    
    if args.prompt:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = input("Enter your prompt: ")

    if prompt == "":
        print("ERR: No prompt provided.")
        sys.exit(1)

    messages = [
    types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )
]
    stop_event = threading.Event()
    spinner_thread = threading.Thread(
        target=spinner,
        args=("Processing your prompt, please wait one moment ", stop_event)
    )

    spinner_thread.start()

    # actual API call
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )

    # stop spinner
    stop_event.set()
    spinner_thread.join()

    # print response
    print(response.text)

    usage = response.usage_metadata
    if verbose and usage:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
    
if __name__ == "__main__":
    main()

