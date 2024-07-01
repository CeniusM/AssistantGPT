from ConsoleHelper import *
from ChatGPT import *
from SmartSpeaker import *
from FileManager import *
from SmartMic import *
from ConversationManager import *
from ConversationTools import *

ConversationManager.convo_setup()
mic = SmartMic()

SmartSpeaker.beep()

while True:

    audio = mic.listen()

    text = mic.interpret_speech(audio)

    if check_text_for_exit(text):
        break

    conversation = ConversationManager.add_and_get(text)

    response = ChatGPT.prompt(conversation)

    SmartSpeaker.play_voice(response)

    ConversationManager.save()


ConversationManager.save(closing=True)
