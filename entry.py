from ConsoleHelper import *
from ChatGPTAgent import *
from SmartSpeaker import *
from FileManager import *
from SmartMic import *
from ConversationManager import *
from conversation_tools import *

agent = ChatGPTAgent()
ConversationManager.convo_setup()

SmartSpeaker.beep()

while True:

    audio = SmartMic.listen()

    text = SmartMic.interpret_speech(audio)

    if check_text(text):
        break

    conversation = ConversationManager.add_and_get(text)

    response = agent.prompt(text)

    SmartSpeaker.play_voice(response)

    ConversationManager.save()


ConversationManager.save(closing=True)
