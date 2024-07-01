from FileManager import *

def load_keys(): 
    return read_json_file("Keys\\sKey")

def get_GPT_key():
    return load_keys()["GPT_KEY"]

def get_EL_key():
    return load_keys()["EL_KEY"]

def load_audio():
    pass