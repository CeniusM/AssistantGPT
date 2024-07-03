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

# if __name__ == "__main__":
#     clean_conversations()
#     renumber_conversations()