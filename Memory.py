from ConversationManager import *
from ChatGPT import *
from ConversationTools import *
from FileManager import *
import os



class Memory:
    #made to manage memory
    def create_response(user_input):
        #create parameters and make api call
        all_summaries_dict = Memory.get_all_summaries()
        conv_numbers = Memory.create_conv_numbers(user_input=user_input, all_summaries_dict=all_summaries_dict)
        conv_data = Memory.get_conv_data(conv_numbers)
        
        #Manage conversation data
        conv_info = Memory.search_through_conversations(user_input, conv_data)
        
        altered_user_input = user_input+"\n Memory info, if needed: "+conv_info
        return altered_user_input
    
    
    def get_all_summaries():
        #first, format conversations
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

    def create_conv_numbers(user_input, all_summaries_dict):
        #create the wanted search info using chatGPT
        search_prompt = f'User input: {user_input}\nAll summaries: {all_summaries_dict}'
        conv_numbers_convo = ConversationManager(promptname="conv_numbers.txt").api_convo_setup(search_prompt)
        conv_numbers = ChatGPT.prompt(conv_numbers_convo, silent=True, temperature=0.2)
        return conv_numbers

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
        search_prompt = f'User input: {user_input}\nConversation data: {conv_data}'
        search_convo = ConversationManager(promptname="search_in_convos.txt").api_convo_setup(search_prompt)
        search_info = ChatGPT.prompt(search_convo, silent=True, temperature=0.2)
        return search_info
    
if __name__ == "__main__":
    print(Memory.create_response("based on what we've talked about earlier, what is your favorite pet?"))