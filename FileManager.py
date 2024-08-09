import json
import os

def read_text_file(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
    except IOError:
        print(f"Error: An I/O error occurred while reading the file at {path}.")
    except Exception as e:
        print(f"Error occurred in FileManager with read_text_file : {e}")
    return ""

def read_json_file(path):
    content = read_text_file(path)
    return json.loads(content)

def write_text_file(path, content):
    with open(path, "w") as file:
        file.write(content)

def write_json_file(path, content):
    try:
        with open(path, "w") as file:
            json.dump(content, file, indent=4)
    except IOError:
        print(f"Error: An I/O error occurred while writing JSON to the file at {path}.")
    except Exception as e:
        print(f"Error occurred in FileManager with write_json_file : {e}")

def path_exists(path):
    return os.path.exists(path)

def create_dir(path):
    return os.makedirs(path)

def join_paths(root, paths):
    return os.path.join(root, paths)