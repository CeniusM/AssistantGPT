from FileManager import *

def load_keys(): 
    return read_json_file("Keys\\sKey")

def get_GPT_key():
    return load_keys()["GPT_KEY"]

def get_EL_key():
    return load_keys()["EL_KEY"]

def get_DMI_key():
    return load_keys()["DMI_KEY"]

def get_WEB_key():
    web_key = load_keys()["WEB_KEY"]
    return web_key["api_key"], web_key["engine_ID"]

def load_audio():
    pass