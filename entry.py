from console import *
from chatGPT_agent import *
from smart_speaker import *

agent = chatGPT_agent()

while True:
    smart_speaker.play_voice("listening")

    audio = "audio_listener"

    text = "speech_to_text"

    response = agent.prompt(text)

    smart_speaker.play_voice(response)
