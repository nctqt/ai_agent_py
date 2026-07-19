# accept a directory path, return a string of the contents of that directory
# make sure the requested directory is inside the working directory

# working directory supplied by us
# directory chosen by LLM

import os

class FileInfo:
    def __init__(self, name, size, dir):
        self.name = str(name)
        self.size = int(size)
        self.dir = bool(dir) 

    def __repr__(self):
        return f"FileInfo(name='{self.name}', size={self.size}, status='{self.dir}')"

def get_files_info(working_directory: str, directory: str = ".") -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.join(abs_working_dir, directory)
    target_dir = os.path.normpath(abs_dir)

    is_valid = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
    if not is_valid: 
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    files_list = []
    try:
        if not os.path.isdir(target_dir):
            return f'Error: "{target_dir}" is not a directory'
        
        for item in os.listdir(target_dir):
            files_list.append(FileInfo(item, os.path.getsize(target_dir + "/" + item), os.path.isdir(target_dir + "/" + item)))
    except Exception as e:
        return f"Error: {e}"


    result = ""
    for file in files_list:
        result += f"- {file.name}: file_size={file.size} bytes, is_dir={file.dir}\n"
    return result