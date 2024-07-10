import re
import os
from FileManager import *
from ConsoleHelper import *
from SmartMic import *
from DMI import *


def check_text(text):
    
    if check_text_for_ambient_noise(text):
        SmartMic.adjust_for_ambient_noise()
        print_bold("Adjusted for ambient noise")

    #if check_text_for_empty(text):
        #return continue

    if check_text_for_web_search(text):
        print_bold("Searching.")
        #text = WebSearch.create_response(text)


    if check_text_for_weather(text):
        print_bold("Getting weather data")
        text = DMI.create_response(text)

    return text


def word_in_text(text, words):
    text = " " + text
    words = [" "+word.lower() for word in words]
    return any(word in text for word in words)



def check_text_for_exit(text):
    #check for exit words
    byewords = ["exit", "quit", "goodbye", "farewell"]
    if word_in_text(text, byewords):
        print_bold("\nGoodbye!\n")
        return True

def check_text_for_ambient_noise(text):
    noise_phrases = ["ambient noise", "background noise", "noise", "støj","støjen", "baggrundsstøj", "baggrundsstøjen" "støjniveau", "støjniveauet", ]
    adjustment_phrases = ["adjust", "update", "change", "calibrate", "correct", "fix", "set", "reset", "kalibrer", "juster", "opdater", "ændre", "ret", "sæt", "nulstil"]
    return word_in_text(text, noise_phrases) and word_in_text(text, adjustment_phrases)


def check_text_for_empty(text):
    if text == " " or text == "":
        print_warning("Did not get what you said (no text)")
        return True
    return False

def check_text_for_weather(text):
    weather_phrases = ["weather", "vejret", "forecast", "prognose", "temperature", "temperatur", "rain", "regn", "wind", "vind", "cloud", "sky", "lightning", "lyn", "snow", "sne", "thunder", "torden", "storm"]
    return word_in_text(text, weather_phrases)


def check_text_for_web_search(text):
    search_phrases = ["search", "google", "look up", "søg", "slå op", "check internet", "check the internet", "check online", "check the web" ]
    return word_in_text(text, search_phrases)




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

    # Function to extract the numeric part from the filename #made by chatgpt
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(0)) if match else 0

    for filename in sorted(os.listdir("Conversations"), key=extract_number): #breaks for more than 9 conversations 10<2

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


def summarize_conversations():

    convnum = 0
    convpath = os.path.join("Conversations\\conversation_"+ str(convnum)+".json")

    while os.path.exists(convpath):

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
                conversation = [message for message in conversation if message["role"] not in Skip_roles]
                summary = ConversationManager.create_summary(conversation)
                conversation.append({"role": "summary", "content": f"{summary}"})
                # write_json_file(convpath, conversation)
                break

        convnum += 1
        convpath = os.path.join("Conversations\\conversation_"+ str(convnum)+".json")

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


if __name__ == "__main__" and True:
    format_conversations()