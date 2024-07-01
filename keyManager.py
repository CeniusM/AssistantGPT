from fileManager import *
import json

def load_keys():
    file = read_text_file("resources\\sKey")
    return json.load(file)

def get_GPT_key():
    return load_keys()["GPT_Key"]

def get_EL_key():
    return load_keys()["EL_Key"]