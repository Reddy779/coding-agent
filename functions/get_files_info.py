
import os
from google.genai import types 


# - README.md: file_size=1032 bytes, is_dir=False
# - src: file_size=128 bytes, is_dir=True
# - package.json: file_size=1234 bytes, is_dir=False

def get_files_info(working_directory, directory="."):

    abs_working_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))
   
    if not abs_directory.startswith(abs_working_dir):
        return f'Error: "{directory}" is not in a working directory'
    
    final_response = ""
    
    contents = os.listdir(abs_directory)
    for content in contents:
        content_path = os.path.join(abs_directory, content) 
        is_dir = os.path.isdir(content_path)
        file_info = os.path.getsize(content_path)
        final_response += f"- {content}: file_size={file_info} bytes, is_dir={is_dir}\n"
    return final_response

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "Get information about a file or list files in a directory "
        "inside the working directory. "
        "If the user mentions a specific file or folder name, "
        "use that exact name as the directory parameter."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The exact file or folder name mentioned by the user, "
                    "relative to the working directory. "
                    "Examples: 'tests.py', 'pkg', '.'"
                ),
            ),
        },
        required=["directory"],
    ),
)