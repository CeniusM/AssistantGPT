from ConversationManager import *



class Memory:
    #made to manage memory
    def create_response(user_input="search the web to figure out how old dolphins can get"):
        #create parameters and make api call
        conv_numbers = Memory.create_conv_numbers(user_input=user_input)
        conv_data = Memory.get_conv_data(conv_numbers)
        
        #Manage conversation data
        conv_info = Memory.search_through_conversations(user_input, conv_data)
        
        altered_user_input = user_input+"\n Memory info, if needed: "+conv_info
        return altered_user_input
    
    

