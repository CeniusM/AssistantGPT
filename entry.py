from ConsoleHelper import *
from ChatGPT import *
from SmartSpeaker import *
from FileManager import *
from SmartMic import *
from ConversationManager import *
from ConversationTools import *
from TextChecker import *

conversation = set_global_conversation_manager()
conversation.convo_setup()
mic = SmartMic()
SmartSpeaker.beep()

try:
    while True:

        text = mic.listen_and_interpret()

        if check_text_for_exit(text): break
        
        conversation.message(USER, text)

        response = ChatGPT.smart_prompt(conversation.formatted())

        SmartSpeaker.play_voice(response)

        conversation.message(AGENT, response)

        conversation.save()

except Exception as e:
    error_handling(e)

conversation.save(closing=True)
print_bold("\nGoodbye!\n")
