from ConsoleHelper import *
from ChatGPT import *
from SmartSpeaker import *
from FileManager import *
from SmartMic import *
from ConversationManager import *
from ConversationTools import *
from TextChecker import *
from Graphics.GUI import *
from ToolManager import get_available_tools

# Set up GUI
gui, thread = GUI.start_async_window(800, 600)
gui.add_user(user="user", alias="You", rgb=(250, 250, 250))
gui.add_user(user="assistant", alias="GPT", rgb=(50, 200, 150))
Listening = (40, 70, 40)
Thinking = (30, 50, 80)
Responding = (40, 40, 40)

# Set up conversations
conversation_manager = set_global_conversation_manager()
conversation_manager.convo_setup()
mic = SmartMic()
SmartSpeaker.beep()

try:
    while gui.running:
        # Get user input
        gui.clear_color = Listening
        text = mic.listen_and_interpret()

        # Parse user input
        if check_text_for_exit(text): break
        
        conversation_formatted = conversation_manager.add_and_get("user", text)
        gui.message("user", text)

        # Generate GPT response
        gui.clear_color = Thinking
        response = ChatGPT.smart_prompt(conversation_formatted, get_available_tools())

        # Play response
        gui.clear_color = Responding
        gui.message("assistant", response)
        conversation_manager.add_paragraph("assistant", response)
        SmartSpeaker.play_voice(response)

        # Backup conversation
        conversation_manager.save()

except Exception as e:
    error_handling(e)

finally:
    conversation_manager.save(closing=True)
    print_bold("\nGoodbye!\n")

    gui.stop()