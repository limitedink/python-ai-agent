import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_path_abs = os.path.abspath(
            os.path.join(working_directory_abs, file_path)
        )

        if not target_path_abs.startswith(working_directory_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        try:
            if not os.path.exists(os.path.dirname(target_path_abs)):
                os.makedirs(os.path.dirname(target_path_abs))
        except Exception as e:
            return f"Error creating directories: {e}"
        try:
            with open(target_path_abs, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception:
            return "Error: write action unsuccessful."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
