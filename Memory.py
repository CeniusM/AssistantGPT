from ConversationManager import *



class Memory:
    #made to manage memory
    def create_response(user_input="search the web to figure out how old dolphins can get"):
        #create parameters and make api call
        all_summaries_dict = Memory.get_all_summaries()
        conv_numbers = Memory.create_conv_numbers(user_input=user_input, all_summaries_dict=all_summaries_dict)
        conv_data = Memory.get_conv_data(conv_numbers)
        
        #Manage conversation data
        conv_info = Memory.search_through_conversations(user_input, conv_data)
        
        altered_user_input = user_input+"\n Memory info, if needed: "+conv_info
        return altered_user_input
    

    def create_conv_numbers(user_input, all_summaries_dict):
        #create the wanted search info using chatGPT
        search_prompt = f'User input: {user_input}\nAll summaries: {all_summaries_dict}'
        conv_numbers_convo = ConversationManager(promptname="conv_numbers.txt").api_convo_setup(search_prompt)
        conv_numbers = ChatGPT.prompt(conv_numbers_convo, silent=True, temperature=0.2)
        return conv_numbers
    
    def get_all_summaries():
        #get all the summaries
        all_summaries_dict = {}
        conv_num = 0
        convo_path = os.path.join("Conversations\\conversation_"+str(conv_num)+".json")
        while os.path.exists(convo_path):
            convo = read_json_file(convo_path)
            summary = convo[-1]["content"]
            all_summaries_dict[conv_num] = summary
            conv_num += 1
        return all_summaries_dict

