from console import *
from chatGPT import *

agent = chatGPT_agent()


while True:
    smart_speaker.play_voice("listening")

    audio = "audio_listener"

    text = "speech_to_text"

    response = agent.send_chat(text)

    smart_speaker.play_voice(response)
