from keyManager import *

class chatGPT_agent:
    def __init__(self):
        self.sKey = getKey()
    
    def send_chat(self, msg: str) -> str:
        pass

    def change_language(self):
        pass

class conventationHandler:
    def get_last_convosation(self):
        pass

    def safe_convosation(self, convo):
        pass

class smart_speaker:    
    def get_language(text) -> str:
        pass

    def play(sound):
        pass

    def play_voice(text):
        lang = smart_speaker.get_language(text)

        sound = api_call(text, lang)

        smart_speaker.play(sound)

        
