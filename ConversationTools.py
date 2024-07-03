import os
from FileManager import *

def check_text_for_exit(text):
    byewords = [" exit", "quit", " goodbye", " farewell"]
    text = " " + text
    if any(word in text for word in byewords):
        return True
    

#functions to look trough the conversations and remove any conversations that only contaion 2 or less elements
def clean_conversations():
    removed_list = []
    for filename in os.listdir("Conversations"):
        path = os.path.join("Conversations", filename)
        convo = read_json_file(path)
        #remove system prompts
        for element in convo:
            if element["role"] == "system" or element["role"] == "Time Tracker":
                convo.remove(element)
            if element["role"] == "Money Tracker":
                price = int(element["Total Cost"].split("$")[0])
                #add the price to the pricecount document in notes +
                total_prize = int(read_text_file("Notes +/pricecount.txt")) + price
                write_text_file("Notes +/pricecount.txt", str(total_prize))
                convo.remove(element)

        if len(convo) < 2:
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
    #list of danish letters
    danish_letters = ["æ", "ø", "å"]
    danish_letters_set = set(danish_letters)
    #list of danish words
    danish_words = ["hvad", "er", "jeg", "du", "vi", "de", "den", "det", "og", "til", "med", "ikke"]
    danish_words_set = set(danish_words)
    #danish_words = ["af", "fordi", "alle", "fra", "kommer", "fri", "kun", "på", "andre", "få", "kunne", "sagde", "at", "gik", "lang", "se", "blev", "glad", "lidt", "selv", "bliver", "godt", "lige", "sidste", "bort", "ham", "lille", "sig", "da", "han", "løb", "sin", "dag", "hans", "man", "sine", "de", "har", "mange", "skal", "dem", "havde", "med", "skulle", "den", "have", "meget", "små", "der", "hele", "men", "som", "deres", "hen", "mere", "stor", "det", "hende", "mig", "store", "dig", "her", "min", "så", "dog", "hjem", "mod", "tid", "du", "hun", "mon", "til", "efter", "hvad", "må", "tog", "eller", "hver", "ned", "ud", "en", "hvis", "nej", "under", "end", "hvor",    "noget", "var", "er", "igen", "nok", "ved", "et", "ikke", "nu", "vi",    "far", "ind", "når", "vil", "fik", "jeg", "og", "ville", "fin", "for", "forbi", "kan"]

    #take set og the response
    letterset = set(text)
    #if the response contains any of these letters, it is danish
    if len(letterset.intersection(danish_letters_set)) > 0:
        return "da-DK"
    
    #take set of the words in the response
    wordset = set(text.split()) 
    #if the response contains any of these words, it is danish
    if len(wordset.intersection(danish_words_set)) > 0:
        return "da-DK"
    
    return "en-US"



# if __name__ == "__main__":
#     clean_conversations()
#     renumber_conversations()