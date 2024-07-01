class SmartSpeaker:    
    def get_language(text) -> str:
        pass

    def play(sound):
        pass

    def beep():
        pass

    def demo_api_call(text, lang):
        pass

    def play_voice(text):
        lang = SmartSpeaker.get_language(text)
        
        sound = SmartSpeaker.demo_api_call(text, lang)

        SmartSpeaker.play(sound)