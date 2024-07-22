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
try:
        
    while True:

        text = mic.listen_and_interpret()

        if check_text_for_exit(text): break
        
        conversation_formatted = conversation_manager.add_and_get("user", text)

        response = ChatGPT.smart_prompt(conversation_formatted)

        SmartSpeaker.play_voice(response)

        conversation_manager.add_paragraph("assistant", response)

        conversation_manager.save()

except Exception as e:
    print_error(f"Something went wrong, closing. Error: {e}")

conversation_manager.save(closing=True)
print_bold("\nGoodbye!\n")