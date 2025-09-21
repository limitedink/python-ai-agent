# Python AI Agent

A production-ready autonomous AI agent built with Google Gemini 2.5 Flash, featuring function calling capabilities, iterative problem-solving, and intelligent task execution. This project demonstrates advanced LLM integration patterns, agent architecture design, and robust error handling in a real-world application.

## Technical Overview

**Core Architecture:** Event-driven agent loop with conversation state management  
**LLM Integration:** Google Gemini 2.5 Flash with function calling API  
**Execution Model:** Iterative feedback loops with bounded execution (max 20 cycles)  
**Security:** Sandboxed file operations within defined working directory  

### Key Features

- **Function Calling System**: Four core operations (file I/O, Python execution) with schema validation
- **Conversation Memory**: Persistent context across multiple tool interactions
- **Error Recovery**: Comprehensive exception handling with graceful degradation
- **Bounded Execution**: Safety mechanisms preventing infinite loops
- **Verbose Logging**: Detailed execution tracing for debugging and monitoring

## Technical Stack

| Component | Technology | Version |
|-----------|------------|----------|
| Runtime | Python | 3.12+ |
| LLM Provider | Google Gemini | 2.5 Flash |
| Package Manager | uv | Latest |
| Environment | dotenv | 1.1.0 |
| API Client | google-genai | 1.12.1 |

## Installation

```bash
git clone https://github.com/your-username/python-ai-agent.git
cd python-ai-agent
uv sync
cp geminiapi.env.example geminiapi.env
# Configure GEMINI_API_KEY in geminiapi.env
```

## Usage

### Command Line Interface

```bash
# Basic execution
uv run main.py "analyze the codebase structure"

# Verbose output with function call tracing
uv run main.py "run tests and analyze results" --verbose

# Interactive mode
uv run main.py
```

### Example Use Cases

**Code Analysis and Documentation:**
```bash
uv run main.py "analyze how the calculator renders output and document the process"
```

**Automated Testing:**
```bash
uv run main.py "run the test suite and fix any failing tests"
```

**File Operations:**
```bash
uv run main.py "create a new feature module with proper error handling"
```

## Architecture

### Agent Loop Design

```
User Input → LLM Decision → Function Execution → Context Update → Iteration
     ↑                                                              ↓
     ←←←←←←←←←←←←← Final Response ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

### Function Calling System

The agent implements a structured function calling framework:

```python
# Function schema definition
schema = types.FunctionDeclaration(
    name="function_name",
    description="Purpose and constraints",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={...},
        required=[...]
    )
)

# Execution pipeline
function_result = call_function(function_call_part, verbose)
validated_result = validate_response_structure(function_result)
conversation_context.append(validated_result)
```

### Available Functions

| Function | Purpose | Security Model |
|----------|---------|----------------|
| `get_files_info` | Directory traversal and file enumeration | Path validation, working directory constraint |
| `get_file_content` | File content retrieval with size limits | Read-only access, content truncation at 10KB |
| `write_file` | File creation and modification | Write access within sandbox, directory creation |
| `run_python_file` | Python script execution | Subprocess isolation, 30-second timeout |

## Implementation Highlights

### Error Handling Strategy

```python
try:
    function_result = function_map[function_name](**function_args)
    return create_success_response(function_result)
except Exception as e:
    return create_error_response(f"Execution failed: {str(e)}")
```

### Conversation State Management

```python
# Maintains full conversation history
messages = [initial_user_message]
for iteration in range(max_iterations):
    response = generate_content(messages)
    messages.append(response.content)
    
    if has_function_calls:
        tool_results = execute_functions(response)
        messages.extend(tool_results)
```

### Security Implementation

- **Path Traversal Prevention**: All file operations validated against working directory
- **Resource Limits**: Execution timeouts and iteration bounds
- **Input Sanitization**: Function arguments validated against schemas
- **Subprocess Isolation**: Python execution in separate process context

## Development

### Project Structure

```
python-ai-agent/
├── main.py                 # Entry point and agent loop
├── functions/              # Function implementations
│   ├── get_files_info.py  # Directory operations
│   ├── get_file_content.py # File reading
│   ├── write_file.py      # File writing
│   └── run_python_file.py # Python execution
├── calculator/            # Sandbox working directory
└── pyproject.toml        # Dependency management
```

### Configuration

**Environment Variables:**
- `GEMINI_API_KEY`: Google Gemini API authentication

**Runtime Parameters:**
- Max iterations: 20
- File size limit: 10KB
- Execution timeout: 30 seconds
- Working directory: `./calculator`

## Performance Characteristics

- **Latency**: ~2-5 seconds per LLM call (depends on function complexity)
- **Throughput**: Optimized for complex multi-step tasks over speed
- **Resource Usage**: Minimal memory footprint, bounded CPU usage
- **Scalability**: Single-threaded design suitable for individual tasks

## Testing

The project includes comprehensive testing scenarios:

```bash
# Run the built-in calculator tests
uv run main.py "execute the test suite and report results"

# Test function calling capabilities
uv run main.py "demonstrate each available function" --verbose
```

## Contributing

Contributions welcome. Please ensure:
- Type hints on all functions
- Comprehensive error handling
- Security validation for file operations
- Documentation for new functions

## License

MIT License - see LICENSE file for details

---

*This project demonstrates production-ready AI agent architecture, LLM integration patterns, and modern Python development practices.*# Python AI Agent

A production-ready autonomous AI agent built with Google Gemini 2.5 Flash, featuring function calling capabilities, iterative problem-solving, and intelligent task execution. This project demonstrates advanced LLM integration patterns, agent architecture design, and robust error handling in a real-world application.

## Technical Overview

**Core Architecture:** Event-driven agent loop with conversation state management  
**LLM Integration:** Google Gemini 2.5 Flash with function calling API  
**Execution Model:** Iterative feedback loops with bounded execution (max 20 cycles)  
**Security:** Sandboxed file operations within defined working directory  

### Key Features

- **Function Calling System**: Four core operations (file I/O, Python execution) with schema validation
- **Conversation Memory**: Persistent context across multiple tool interactions
- **Error Recovery**: Comprehensive exception handling with graceful degradation
- **Bounded Execution**: Safety mechanisms preventing infinite loops
- **Verbose Logging**: Detailed execution tracing for debugging and monitoring

## Technical Stack

| Component | Technology | Version |
|-----------|------------|----------|
| Runtime | Python | 3.12+ |
| LLM Provider | Google Gemini | 2.5 Flash |
| Package Manager | uv | Latest |
| Environment | dotenv | 1.1.0 |
| API Client | google-genai | 1.12.1 |

## Installation

```bash
git clone https://github.com/your-username/python-ai-agent.git
cd python-ai-agent
uv sync
cp geminiapi.env.example geminiapi.env
# Configure GEMINI_API_KEY in geminiapi.env
```

## Usage

### Command Line Interface

```bash
# Basic execution
uv run main.py "analyze the codebase structure"

# Verbose output with function call tracing
uv run main.py "run tests and analyze results" --verbose

# Interactive mode
uv run main.py
```

### Example Use Cases

**Code Analysis and Documentation:**
```bash
uv run main.py "analyze how the calculator renders output and document the process"
```

**Automated Testing:**
```bash
uv run main.py "run the test suite and fix any failing tests"
```

**File Operations:**
```bash
uv run main.py "create a new feature module with proper error handling"
```

## Architecture

### Agent Loop Design

```
User Input → LLM Decision → Function Execution → Context Update → Iteration
     ↑                                                              ↓
     ←←←←←←←←←←←←← Final Response ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

### Function Calling System

The agent implements a structured function calling framework:

```python
# Function schema definition
schema = types.FunctionDeclaration(
    name="function_name",
    description="Purpose and constraints",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={...},
        required=[...]
    )
)

# Execution pipeline
function_result = call_function(function_call_part, verbose)
validated_result = validate_response_structure(function_result)
conversation_context.append(validated_result)
```

### Available Functions

| Function | Purpose | Security Model |
|----------|---------|----------------|
| `get_files_info` | Directory traversal and file enumeration | Path validation, working directory constraint |
| `get_file_content` | File content retrieval with size limits | Read-only access, content truncation at 10KB |
| `write_file` | File creation and modification | Write access within sandbox, directory creation |
| `run_python_file` | Python script execution | Subprocess isolation, 30-second timeout |

## Implementation Highlights

### Error Handling Strategy

```python
try:
    function_result = function_map[function_name](**function_args)
    return create_success_response(function_result)
except Exception as e:
    return create_error_response(f"Execution failed: {str(e)}")
```

### Conversation State Management

```python
# Maintains full conversation history
messages = [initial_user_message]
for iteration in range(max_iterations):
    response = generate_content(messages)
    messages.append(response.content)
    
    if has_function_calls:
        tool_results = execute_functions(response)
        messages.extend(tool_results)
```

### Security Implementation

- **Path Traversal Prevention**: All file operations validated against working directory
- **Resource Limits**: Execution timeouts and iteration bounds
- **Input Sanitization**: Function arguments validated against schemas
- **Subprocess Isolation**: Python execution in separate process context

## Development

### Project Structure

```
python-ai-agent/
├── main.py                 # Entry point and agent loop
├── functions/              # Function implementations
│   ├── get_files_info.py  # Directory operations
│   ├── get_file_content.py # File reading
│   ├── write_file.py      # File writing
│   └── run_python_file.py # Python execution
├── calculator/            # Sandbox working directory
└── pyproject.toml        # Dependency management
```

### Configuration

**Environment Variables:**
- `GEMINI_API_KEY`: Google Gemini API authentication

**Runtime Parameters:**
- Max iterations: 20
- File size limit: 10KB
- Execution timeout: 30 seconds
- Working directory: `./calculator`

## Performance Characteristics

- **Latency**: ~2-5 seconds per LLM call (depends on function complexity)
- **Throughput**: Optimized for complex multi-step tasks over speed
- **Resource Usage**: Minimal memory footprint, bounded CPU usage
- **Scalability**: Single-threaded design suitable for individual tasks

## Testing

The project includes comprehensive testing scenarios:

```bash
# Run the built-in calculator tests
uv run main.py "execute the test suite and report results"

# Test function calling capabilities
uv run main.py "demonstrate each available function" --verbose
```

## Contributing

Contributions welcome. Please ensure:
- Type hints on all functions
- Comprehensive error handling
- Security validation for file operations
- Documentation for new functions

## License

MIT License - see LICENSE file for details

---

*This project demonstrates production-ready AI agent architecture, LLM integration patterns, and modern Python development practices.*
