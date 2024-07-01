import os
import json
from FileManager import *
import time

class ConversationManager:
    def __init__(self):
        self.conversation = None
        pass

    def convo_setup(self, *conversation_IDs):
        conversation = []
        for ID in conversation_IDs:
            convo_path = os.path.join("conversation", ID + ".json")
            if os.path.exists(convo_path):
                conversation.append(read_json_file(convo_path))
            else:
                print(f"Error: The file at {convo_path} was not found.")

        conversation_name = self.conversation_name()
        self.save(conversation, conversation_name)
        return conversation

        
    def conversation_name(self):
        conv_foldername = 'conversations'
        base_filename = 'conversation'
        suffix = 0
        filename = os.path.join(conv_foldername, f'{base_filename}_{suffix}.txt')

        while os.path.exists(filename):
            suffix += 1
            filename = os.path.join(conv_foldername, f'{base_filename}_{suffix}.txt')

        return filename

    def save(self, path=None, closing=False):
        if path != None:
            #saves the conversation to a json file
            write_json_file(path, self.conversation)

        if closing:
            #adds on the prize and the date and time at the end of the json file
            self.conversation.append({"role": "Time Tracker", "Time and day": f"{time.asctime(time.localtime(time.time()))}"})
            self.conversation.append({"role": "Money Tracker", "Total Cost": f"{self.total_cost}$"})

    def add_paragraph(self, text):
        pass

    def get_conversation(self):
        pass

    def add_and_get(self, text):
        self.add_paragraph(text)
        return self.get_conversation()
    
if __name__ == "__main__":
    print(ConversationManager().conversation_name())