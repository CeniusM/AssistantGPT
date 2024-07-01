from ConsoleHelper import *
from ChatGPTAgent import *
from SmartSpeaker import *
from FileManager import *
from SmartMic import *
from ConversationManager import *

agent = ChatGPTAgent()

SmartSpeaker.beep()

while True:

    audio = SmartMic.listen()

    text = SmartMic.interpret_speech(audio)

    conversation = ConversationManager.update_and_get_conversation(text)

    response = agent.prompt(text)

    SmartSpeaker.play_voice(response)
