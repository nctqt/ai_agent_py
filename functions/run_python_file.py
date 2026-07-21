
import os, subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file = os.path.join(abs_working_dir, file_path)
        norm_file = os.path.normpath(abs_file)

        is_valid = os.path.commonpath([abs_working_dir, norm_file]) == abs_working_dir
        if not is_valid: 
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        is_file = os.path.isfile(norm_file)
        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", norm_file]
        if args:
            command.extend(args)
        run_output = subprocess.run(command, timeout=30, capture_output=True, text=True, cwd=abs_working_dir)

        output = ""
        if run_output.returncode != 0:
            output += f"Process exited with code {run_output.returncode}\n"
        output += f"STDOUT: {run_output.stdout}"
        output += f"STDERR: {run_output.stderr}"

    except Exception as e:
        return f"Error: {e}"
    
    return output

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file, relative to the working directory",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "list of command line arguments"
                }
            },
        },
    },
}