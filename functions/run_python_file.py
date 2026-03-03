
import os
import subprocess
from google.genai import types 


def run_python_file(working_directory: str, file_path: str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
   
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in a working directory'
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"
    
    if not file_path.endswith(".py"):
        return f"Error: {file_path} is not a python file."
    
    try:
        final_args = ["python", file_path]
        final_args.extend(args)
        output = subprocess.run(
            final_args,
            cwd=abs_working_dir, 
            capture_output=True,
            text=True,
            timeout=30
        )
        final_string =  f""" 
STDOUT: {output.stdout}
STDERR: {output.stderr}
"""
        if output.stdout and output.stderr:
            final_string = "No output produced. \n"
        if output.returncode != 0:
            final_string += f"Process exited with code {output.returncode}"
        return final_string
    except Exception as e:
        return f"Error: executing python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Execute a Python file inside the working directory. "
        "If the user says 'run <file>.py' or asks to execute a Python script, "
        "use this function."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The exact Python file name mentioned by the user. "
                    "Example: 'tests.py', 'main.py'"
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the script.",
            ),
        },
        required=["file_path"],
    ),
)