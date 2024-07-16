import os
from FileManager import *
import time
from ChatGPT import *

class ConversationManager:
    def __init__(self, promptname="assistantP.txt"):
        self.conversation = []
        self.messages = []
        self.conversation_name = self.conversation_name()
        self.system_prompt = read_text_file("Prompts\\"+promptname)

    def api_message_setup(self, user_input = None, api_data = None):
        self.conversation.append({"role": "system", "content": self.system_prompt})
        if user_input != None:
            self.conversation.append({"role": "user", "content": str(user_input)})
        if api_data != None:
            self.conversation.append({"role": "tool", "content": str(api_data)})
        return self.conversation

    def api_convo_setup(self, api_data = None):
        convo = self.conversation.copy()
        convo.pop(0)
        convo.insert( len(convo) - 1 , {"role": "system", "content": self.system_prompt})
        if api_data != None:
            convo.append({"role": "tool", "content": str(api_data)})
        return convo


    def convo_setup(self, *conversation_IDs):
        self.conversation.append({"role": "system", "content": self.system_prompt})
        for ID in conversation_IDs:
            convo_path = os.path.join("Conversations\\conversation_"+str(ID)+".json")
            if os.path.exists(convo_path):
                self.conversation.append(read_json_file(convo_path))
            else:
                print(f"Error: The file at {convo_path} was not found.")

        self.save()

    def conversation_name(self):
        conv_foldername = 'Conversations'
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

            summary_conversation = self.conversation.copy()
            summary = ConversationManager.create_summary(summary_conversation)

            #adds on the prize and the date and time at the end of the json file
            self.conversation.append({"role": "Time Tracker", "Time and day": f"{time.asctime(time.localtime(time.time()))}"})
            self.conversation.append({"role": "Money Tracker", "Total Cost": f"{ChatGPT.total_cost}$"})
            self.conversation.append({"role": "summary", "content": f"{summary}"})
        
        write_json_file(path, self.conversation)

    def create_summary(summary_conversation):
    #Make the summarytext from the summary_conversation
        summary_conversation.pop(0)
        summary_conversation.append({"role": "system", "content":"make a super breaf summary of what this converation was about, ignore time and money modules if any. Include the discussed topic points. Use at max 1-2 short sentences"})
        summary = ChatGPT.prompt(summary_conversation, silent=True, temperature=0.2)
        return summary

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
    