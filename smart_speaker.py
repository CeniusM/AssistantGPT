class smart_speaker:    
    def get_language(text) -> str:
        pass

    def play(sound):
        pass

    def demo_api_call(text, lang):
        pass

    def play_voice(text):
        lang = smart_speaker.get_language(text)
        
        sound = smart_speaker.demo_api_call(text, lang)

        smart_speaker.play(sound)