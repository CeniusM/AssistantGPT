from ConversationManager import *
from FileManager import *
from ConsoleHelper import *

import os
import ast


class Memory:
    #made to manage memory
    def create_response():
        print_bold("Checking memory")

        #create parameters and make api call
        all_summaries_dict = Memory.get_all_summaries()
        conv_numbers = Memory.create_conv_numbers(all_summaries_dict)
        filtered_conv_numbers = Memory.filter_conv_numbers(conv_numbers)

        #Get and manage conversation data
        conv_data = Memory.get_conv_data(filtered_conv_numbers)
        conv_info = Memory.search_through_conversations(conv_data)
        
        return conv_info
    
    
    def get_all_summaries():
        #first, format conversations
        from ConversationTools import format_conversations
        format_conversations()

        #get all the summaries
        all_summaries_dict = {}
        conv_num = 0
        convo_path = os.path.join("Conversations\\conversation_"+str(conv_num)+".json")
        while os.path.exists(convo_path):
            convo = read_json_file(convo_path)
            if convo[-1]["role"] == "summary":
                summary = convo[-1]["content"]
                all_summaries_dict[conv_num] = summary
            conv_num += 1
            convo_path = os.path.join("Conversations\\conversation_"+str(conv_num)+".json")

        return all_summaries_dict

    def create_conv_numbers(all_summaries_dict):
        #create the wanted search info using chatGPT

        conversation_history = [ #for now - debug
        {"role": "system", "content": "You are a helpful assistant."},
        #{"role": "user", "content": "What's the weather like today?"}
        {"role": "user", "content" : "based on what we've talked about earlier, what is your favorite pet"}
    ]
        conv_numbers_convo = ConversationManager(promptname="conv_numbers.txt").api_convo_setup(conversation_history, all_summaries_dict)
        conv_numbers = ChatGPT.prompt(conv_numbers_convo)

        return conv_numbers
        
    def filter_conv_numbers(conv_numbers):
        
        #check if the conv_numbers are already a list or number
        try:
            conv_numbers_eval =  ast.literal_eval(conv_numbers)
            if type(conv_numbers_eval) == int:
                return [conv_numbers_eval]
            elif type(conv_numbers_eval) == list:
                return conv_numbers_eval
        except:
            pass
        #filter any non-numeric characters
        if conv_numbers != "None":
            formatted_conv_numbers = []
            for char in conv_numbers.split():
                char = char.replace(".", "")
                if char.isnumeric():
                    formatted_conv_numbers.append(int(char))
        
        return formatted_conv_numbers


    def get_conv_data(conv_numbers):
        #get the conversation data
        conv_data = []
        for conv_num in conv_numbers:
            convo_path = os.path.join("Conversations\\conversation_"+str(conv_num)+".json")
            if os.path.exists(convo_path):
                convo = read_json_file(convo_path)
                conv_data.append(convo)
            else:
                print(f"Error: The file at {convo_path} was not found.")
        return conv_data

    def search_through_conversations(user_input, conv_data):
        #use the conversation data to and ChatGPT to search through the conversations
        from ChatGPT import prompt
        search_convo = ConversationManager(promptname="search_in_convos.txt").api_convo_setup(conv_data)
        search_info = ChatGPT.prompt(search_convo)
        return search_info
    
if __name__ == "__main__":
    # print(Memory.create_response("based on what we've talked about earlier, how old am i?"))
    print(Memory.create_response("based on what we've talked about earlier, what is your favorite pet?"))