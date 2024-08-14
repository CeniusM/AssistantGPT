from ConsoleHelper import *
from ChatGPT import *
from SmartSpeaker import *
from FileManager import *
from SmartMic import *
from ConversationManager import *
from ConversationTools import *
from TextChecker import *
from Graphics.GUI import *

gui, thread = GUI.start_async_window(800, 600)

conversation_manager = set_global_conversation_manager()
conversation_manager.convo_setup()
mic = SmartMic()
SmartSpeaker.beep()

try:
    while gui.running:

        gui.clear_color = (40, 80, 80)
        text = mic.listen_and_interpret()
        gui.clear_color = (100, 60, 60)

        if check_text_for_exit(text): break
        
        conversation_formatted = conversation_manager.add_and_get("user", text)
        gui.message("You", text)

        response = ChatGPT.smart_prompt(conversation_formatted)
        gui.clear_color = (40, 40, 40)

        gui.message("GPT", response)
        conversation_manager.add_paragraph("assistant", response)
        SmartSpeaker.play_voice(response)

        conversation_manager.save()

except Exception as e:
    error_handling(e)

finally:
    conversation_manager.save(closing=True)
    print_bold("\nGoodbye!\n")

    gui.stop()