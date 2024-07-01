import json

def read_text_file(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
    except IOError:
        print(f"Error: An I/O error occurred while reading the file at {path}.")
    return ""

def read_json_file(path):
    file = read_text_file(path)
    return json.loads(file)