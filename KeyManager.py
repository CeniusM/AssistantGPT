from FileManager import *
import json

def load_keys():
    file = read_text_file("Keys\\sKey")
    return json.loads(file)

def get_GPT_key():
    return load_keys()["GPT_KEY"]

def get_EL_key():
    return load_keys()["EL_KEY"]

def load_audio():
    pass