def read_text_file(path: str) -> str:
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
    except IOError:
        print(f"Error: An I/O error occurred while reading the file at {path}.")
    return ""