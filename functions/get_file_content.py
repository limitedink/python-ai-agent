from google.genai import types


def get_file_content(working_directory, file_path):
    import os

    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))

        wd_prefix = working_directory_abs.rstrip(os.sep) + os.sep
        if not target_abs.startswith(wd_prefix):
            return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

        if not os.path.isfile(target_abs):
            return f"Error: '{file_path}' is not a file"

        try:
            from functions.config import MAX_CHARS
        except Exception:
            # Fallback relative import for some execution contexts
            from .config import MAX_CHARS

        # Read up to MAX_CHARS + 1 to detect truncation
        with open(target_abs, "r") as f:
            data = f.read(MAX_CHARS + 1)

        if len(data) > MAX_CHARS:
            data = (
                data[:MAX_CHARS]
                + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
        return data
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
