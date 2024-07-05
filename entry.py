from ConsoleHelper import *
from ChatGPT import *
from SmartSpeaker import *
from FileManager import *
from SmartMic import *
from ConversationManager import *
from ConversationTools import *

conversation_manager = ConversationManager()
conversation_manager.convo_setup()
mic = SmartMic()
running = True  #MAKE CHECK TEXT CHECK FOR Text == None AND SET RUNNING TO FALSE

SmartSpeaker.beep()

while running:
    audio = mic.listen()

    text = mic.interpret_speech(audio)

    if text is None:
        print_warning("Did not get what you said (no text)")
        continue

    if check_text(text): #MAKE THIS FUNCTION CHECK FOR Text == None AND SET RUNNING TO FALSE
        break

    conversation_formatted = conversation_manager.add_and_get("user", text)

    response = ChatGPT.prompt(conversation_formatted)

    SmartSpeaker.play_voice(response)

    conversation_manager.add_paragraph("assistant", response)

    conversation_manager.save()

conversation_manager.save(closing=True)
print_bold("\nGoodbye!\n")