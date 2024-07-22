from FileManager import *
from ConsoleHelper import *
from ChatGPT import *
from ConversationManager import *

import re
import os


#functions to look trough the conversations and remove any conversations that only contaion 2 or less elements
def clean_conversations():
    removed_list = []
    for filename in os.listdir("Conversations"):
        path = os.path.join("Conversations", filename)
        convo = read_json_file(path)
        
        Skip_roles = ["system", "Time Tracker", "Money Tracker"]
        formatted_convo = [message for message in convo if message["role"] not in Skip_roles]

        if len(formatted_convo) < 2:
            os.remove(path)
            filenum = int(filename.split("_")[1].split(".")[0])
            removed_list.append(filenum)
    print(f"Removed conversations: {removed_list}")
    
# renumber the files
def renumber_conversations():
    current_num = 0
    renumbered = False

    # Function to extract the numeric part from the filename to sort properly   #made by chatgpt
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(0)) if match else 0
    
    # Get the current conversation number from the global conversation manager
    conversation_manager = set_global_conversation_manager()
    current_conversation_name = conversation_manager.conversation_name
    current_conversation_num = int(current_conversation_name.split("_")[1].split(".")[0])

    for filename in sorted(os.listdir("Conversations"), key=extract_number):

        filenum = int(filename.split("_")[1].split(".")[0])
        if filenum == current_num:
            current_num += 1
            continue

        path = os.path.join("Conversations", filename)
        new_filename = f"conversation_{current_num}.json"
        new_path = os.path.join("Conversations", new_filename)
        os.rename(path, new_path)
        print(f"{filenum} -> {current_num}")
        if filenum == current_conversation_num:
            conversation_manager.conversation_name = new_path

        renumbered = True
        current_num += 1

    if renumbered:
        print("Renumbered all conversations")


def summarize_conversations():

    convnum = 0
    summarized = False
    convpath = os.path.join("Conversations\\conversation_"+ str(convnum)+".json")

    conversation_manager = set_global_conversation_manager()
    current_conversation_name = conversation_manager.conversation_name

    while os.path.exists(convpath) and convpath != current_conversation_name:

        conversation = read_json_file(convpath)
        
        while True:
            conv_obj = conversation.pop()
            role = conv_obj["role"]

            if role == "summary":
                break
            else:
                conversation.append(conv_obj)
                #remove "money tracker" and "time tracker" from the conversation
                Skip_roles = ["Time Tracker", "Money Tracker"]
                summary_conversation = [message for message in conversation if message["role"] not in Skip_roles]

                summary = ConversationManager.create_summary(summary_conversation)
                conversation.append({"role": "summary", "content": f"{summary}"})
                write_json_file(convpath, conversation)
                summarized = True
                break

        convnum += 1
        convpath = os.path.join("Conversations\\conversation_"+ str(convnum)+".json")

    if summarized:
        print("Summarized all conversations\n")


def format_conversations():
    clean_conversations()
    renumber_conversations()
    summarize_conversations()


#method for finding if the langeuage of the response is danish or english, for the synthesized reader
def get_text_language(text):
    danish_letters_set = set(["æ", "ø", "å"])
    danish_words_set = set(["hvad", "er", "jeg", "du", "vi", "de", "den", "det", "og", "til", "med", "ikke"])
    
    if len(set(text).intersection(danish_letters_set)) > 0: #if the response contains any of these letters, it is danish
        return "da-DK"   
    if len(set(text.split()).intersection(danish_words_set)) > 0:  #if the response contains any of these words, it is danish
        return "da-DK"
    
    return "en-US"

def print_conversation(num):

    path = os.path.join("Conversations", f"conversation_{num}.json")
    conversation = read_json_file(path)
    print_bold(f"Conversation {num}:\n\n")

    for message in conversation:
        role = message["role"]
        
        if role == "user":
            print_info(f"User: {message["content"]}\n")
        elif role == "assistant":
            print_good(f"Assistant: {message["content"]}\n")



if __name__ == "__main__" and True:
    format_conversations()
