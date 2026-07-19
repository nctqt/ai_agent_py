
import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file = os.path.join(abs_working_dir, file_path)
        norm_file = os.path.normpath(abs_file)

        is_valid = os.path.commonpath([abs_working_dir, norm_file]) == abs_working_dir
        if not is_valid: 
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        is_dir = os.path.isdir(norm_file)
        if is_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent = os.path.dirname(norm_file)
        os.makedirs(parent, exist_ok=True)

        with open(norm_file, "w") as f:
            f.write(content)

    except Exception as e:
        return f"Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'