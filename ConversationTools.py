import os
from FileManager import *
from ConsoleHelper import *
from SmartMic import *

def check_text(text):
    #check for exit words
    byewords = [" exit", "quit", " goodbye", " farewell"]
    text = " " + text
    if any(word in text for word in byewords):
        #SET RUNNING TO FALSE, BUT HOW?
        return True
    
    # #check for empty text
    # if text == " ":
    #     print_warning("Did not get what you said (no text)")
    #     return True

    # check for ambient noise adjustment
    noise_phrases = ["ambient noise", "background noise", "noise", "støj","støjen", "baggrundsstøj", "baggrundsstøjen" "støjniveau", "støjniveauet", ]
    adjustment_phrases = ["adjust", "update", "change", "calibrate", "correct", "fix", "set", "reset", "kalibrer", "juster", "opdater", "ændre", "ret", "sæt", "nulstil"]
    if any(word in text for word in noise_phrases) and any(word in text for word in adjustment_phrases):
        SmartMic.adjust_for_ambient_noise()
        print_bold("Adjusted for ambient noise")
    
    return False


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
            print(f"Removed {filename}")
    print(f"Removed {removed_list}")
    
# renumber the files
def renumber_conversations():
    current_num = 0
    print("Renumbering conversations")
    for filename in os.listdir("Conversations"):

        filenum = int(filename.split("_")[1].split(".")[0])
        if filenum == current_num:
            current_num += 1
            continue

        path = os.path.join("Conversations", filename)
        new_filename = f"conversation_{current_num}.json"
        new_path = os.path.join("Conversations", new_filename)
        os.rename(path, new_path)
        print(f"{filenum} -> {current_num}")
        current_num += 1
    print("Renumbered all conversations")


#method for finding if the langeuage of the response is danish or english, for the synthesized reader
def get_text_language(text):
    danish_letters_set = set(["æ", "ø", "å"])
    danish_words_set = set(["hvad", "er", "jeg", "du", "vi", "de", "den", "det", "og", "til", "med", "ikke"])
    
    #if the response contains any of these letters, it is danish
    if len(set(text).intersection(danish_letters_set)) > 0:
        return "da-DK"

    #if the response contains any of these words, it is danish
    if len(set(text.split()).intersection(danish_words_set)) > 0:
        return "da-DK"
    
    return "en-US"


if __name__ == "__main__" and True:
    clean_conversations()
    renumber_conversations()