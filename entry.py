from console import *
from chatGPT import *
from smartSpeaker import *
from smart_mic import *

agent = chatGPT_agent()

smart_speaker.play_voice("listening")

while True:

    audio = smart_mic.listen()

    text = "speech_to_text"

    response = agent.prompt(text)

    smart_speaker.play_voice(response)
