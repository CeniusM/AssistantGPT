from console import *
from chatGPT_agent import *
from smart_speaker import *
from file_manager import *

agent = chatGPT_agent()

smart_speaker.beep()

while True:
    audio = "audio_listener"

    text = "speech_to_text"

    response = agent.prompt(text)

    smart_speaker.play_voice(response)
