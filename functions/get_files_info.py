import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        if not full_path.startswith(working_directory):
            return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
        if os.path.isdir(full_path) == False:
            return f"Error: '{directory}' is not a directory"

        items = []
        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)
            try:
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                items.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                items.append(f"- {entry}: Error: {e}")
        print(f"Result for {directory} directory:")
        return "\n".join(items)

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
