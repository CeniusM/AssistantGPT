from ConsoleHelper import *
from ChatGPT import *
from SmartSpeaker import *
from FileManager import *
from SmartMic import *
from ConversationManager import *
from ConversationTools import *
from TextChecker import *

conversation_manager = set_global_conversation_manager()

conversation_manager.convo_setup()
mic = SmartMic()

SmartSpeaker.beep()

while True:
    audio = mic.listen()

    text = mic.interpret_speech(audio)

    if text is None:
        print_warning("Did not get what you said (no text)")
        continue

    if check_text_for_exit(text):
        break
    # text = check_text(text)

    conversation_formatted = conversation_manager.add_and_get("user", text)

    response = ChatGPT.smart_prompt(conversation_formatted)

    SmartSpeaker.play_voice(response)

    conversation_manager.add_paragraph("assistant", response)

    conversation_manager.save()

conversation_manager.save(closing=True)
print_bold("\nGoodbye!\n")