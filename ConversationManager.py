import os
from FileManager import *
import time

class ConversationManager:
    def __init__(self):
        self.conversation = None
        self.conversation_name = self.conversation_name()

    def convo_setup(self, *conversation_IDs):
        self.conversation = []
        for ID in conversation_IDs:
            convo_path = os.path.join("Conversations\\conversation_"+str(ID)+".json")
            if os.path.exists(convo_path):
                self.conversation.append(read_json_file(convo_path))
            else:
                print(f"Error: The file at {convo_path} was not found.")

        self.save()
        #return self.conversation

        
    def conversation_name(self):
        conv_foldername = 'conversations'
        base_filename = 'conversation'
        suffix = 0
        filename = os.path.join(conv_foldername, f'{base_filename}_{suffix}.json')


        while os.path.exists(filename):
            suffix += 1
            filename = os.path.join(conv_foldername, f'{base_filename}_{suffix}.json')

        return filename

    def save(self, closing=False):
        path = self.conversation_name

        if closing:
            #adds on the prize and the date and time at the end of the json file
            self.conversation.append({"role": "Time Tracker", "Time and day": f"{time.asctime(time.localtime(time.time()))}"})
            #self.conversation.append({"role": "Money Tracker", "Total Cost": f"{self.total_cost}$"})
        
        write_json_file(path, self.conversation)

    def add_paragraph(self, role, content:str):
        formatted_text = {"role": role, "content": content}       
        self.conversation.append(formatted_text)
        return self.conversation

    def get_conversation_formatted(self):
        convo = self.conversation.copy()  # Copy the original list to avoid modifying it directly
        
        if len(convo) < 2:  # If there are less than 2 elements, no rearrangement is needed
            return convo

        header = convo.pop(0)  # Remove the first element (header)
        convo.insert(len(convo) - 1, header)  # Insert the header before the last element
        
        return convo  # Return the modified list

    def add_and_get(self, role, content):
        self.add_paragraph(role, content)
        return self.get_conversation_formatted()
    
if __name__ == "__main__":
    cm = ConversationManager()
    cm.convo_setup(2)
    cm.save(closing=True)