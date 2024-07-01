from console import *
from chatGPT import *
from smartSpeaker import *

agent = chatGPT_agent()

while True:
    smart_speaker.play_voice("listening")

    audio = "audio_listener"

    text = "speech_to_text"

    response = agent.prompt(text)

    smart_speaker.play_voice(response)
