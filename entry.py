from console import *
from chatGPT_agent import *
from smart_speaker import *
from file_manager import *
from smart_mic import *
from ConversationManager import *

agent = chatGPT_agent()

SmartSpeaker.beep()

while True:

    audio = SmartMic.listen()

    text = SmartMic.interpret_speech(audio)

    conversation = ConversationManager.update_and_get_conversation(text)

    response = agent.prompt(text)

    SmartSpeaker.play_voice(response)
