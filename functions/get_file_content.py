
import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file = os.path.join(abs_working_dir, file_path)
        norm_file = os.path.normpath(abs_file)

        is_valid = os.path.commonpath([abs_working_dir, norm_file]) == abs_working_dir
        if not is_valid: 
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        is_file = not os.path.isdir(norm_file)
        if not is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000
        # print(norm_file)
        with open(norm_file, "r") as f:
            content = f.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    except Exception as e:
        return f"Error: {e}"
    
    return content
