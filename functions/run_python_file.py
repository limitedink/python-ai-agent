import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory, file_path))

        # Security check: ensure file is within working directory
        if not target_abs.startswith(working_directory_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file exists
        if not os.path.exists(target_abs):
            return f'Error: File "{file_path}" not found.'

        # Check if file is a Python file
        if not target_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Build command: python3 + file_path + args
        cmd = ["python3", file_path] + args

        try:
            # Execute the Python file
            completed_process = subprocess.run(
                cmd,
                cwd=working_directory_abs,
                timeout=30,
                capture_output=True,
                text=True,
            )

            # Get stdout and stderr
            stdout = completed_process.stdout or ""
            stderr = completed_process.stderr or ""

            # Build output string
            output_string = []
            if stdout.strip():
                output_string.append(f"STDOUT: {stdout.strip()}")
            if stderr.strip():
                output_string.append(f"STDERR: {stderr.strip()}")

            # Check for non-zero exit code
            if completed_process.returncode != 0:
                output_string.append(
                    f"Process exited with code {completed_process.returncode}"
                )

            # Return formatted output or "No output produced."
            if output_string:
                return "\n".join(output_string)
            else:
                return "No output produced."

        except subprocess.TimeoutExpired:
            return "Error: executing Python file: Process timed out after 30 seconds"
        except Exception as e:
            return f"Error: executing Python file: {e}"

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
