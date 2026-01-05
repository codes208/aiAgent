import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, abs_file_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]

        if args != None:
            command.extend(args)

        run_command = subprocess.run(command,
                                     cwd=working_dir_abs,
                                     capture_output=True,
                                     text=True,
                                     timeout=30
                                     )
        output_string = []
        if run_command.returncode != 0:
            output_string.append(f"Process exited with code {run_command.returncode}")
        if not run_command.stderr and not run_command.stdout:
            output_string.append(f"No output produced")
        if run_command.stdout or run_command.stderr:
            if run_command.stdout:
                output_string.append(f"STDOUT: {run_command.stdout}")
            if run_command.stderr:
                output_string.append(f"STDERR: {run_command.stderr}")

        return "\n".join(output_string)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file on a given file_path, returning a string list containing output to stderr, stdout, and exit codes. Optionally accepts a list of command-line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python file",
                items=types.Schema(
                    type=types.Type.STRING,
                    )
                
                )
        },
    ),
)
