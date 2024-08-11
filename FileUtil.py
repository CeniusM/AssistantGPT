# Temp idea for better clarity when working with files and paths

from varname import nameof

import json
import os

from ConsoleHelper import print_error

class File:
    def read_text(path):
        try:
            with open(path, 'r') as file:
                return file.read()
        except Exception as e:
            print_error(f"Error at {nameof(File.read_text)}: {str(e)}")
            return None

    def read_json(path):
        try:
            content = File.read_text(path)
            return json.loads(content)
        except Exception as e:
            print_error(f"Error at {nameof(File.read_json)}: {str(e)}")
            return {}

    def write_text(path, content):
        try:
            with open(path, "w") as file:
                file.write(content)
        except Exception as e:
            print_error(f"Error at {nameof(File.write_text)}: {str(e)}")

    def write_json(path, content):
        try:
            with open(path, "w") as file:
                json.dump(content, file, indent=4)
        except Exception as e:
            print_error(f"Error at {nameof(File.write_json)}: {str(e)}")

class Path:
    def exists(path):
        return os.path.exists(path)

    def join(root, paths):
        return os.path.join(root, paths)

    def create_dir(path):
        return os.makedirs(path)