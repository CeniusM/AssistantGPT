from ConsoleHelper import *
from ChatGPT import *
from SmartSpeaker import *
from FileManager import *
from SmartMic import *
from ConversationManager import *

agent = ChatGPT()
mic = SmartMic()

SmartSpeaker.beep()

while True:

    audio = mic.listen()

    text = mic.interpret_speech(audio)

    conversation = ConversationManager.add_and_get(text)

    response = agent.prompt(text)

    SmartSpeaker.play_voice(response)
