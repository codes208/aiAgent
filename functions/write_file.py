import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, abs_file_path]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        directory_path = os.path.dirname(abs_file_path)
        os.makedirs(directory_path, exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing to file "{file_path}": {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Opens a file for writing and returns a string on completion",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path","content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a file, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that is to be written to the file"
                )
        },
    ),
)
