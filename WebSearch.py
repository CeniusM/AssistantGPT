from ConversationManager import *
from ConsoleHelper import *

class WebSearch:
        
    def create_response(user_input="search the web to figure out how old dolphins can get", search_query=None):
        print_bold("Searching.")
        
        #create parameters and make api call
        if search_query == None:
            search_query = WebSearch.create_search_query(user_input=user_input)
        dependencies = WebSearch.create_dependencies(search_query)
        api_data = WebSearch.api_call(dependencies)

        #convert the data from the search
        converted_data = WebSearch.convert_api_data(api_data)
        search_info = WebSearch.manage_data(converted_data)
        
        return search_info


    def create_search_query(user_input):
        #create the wanted search info using chatGPT
        search_query_convo = ConversationManager(promptname="search_query.txt").api_message_setup(user_input=user_input)
        search_query = ChatGPT.prompt(search_query_convo)
        return search_query
    
    def create_dependencies(search_query):
        #create the wanted search info using chatGPT
        print("memory nonceno nice")


if __name__ == "__main__":
    print(WebSearch.create_search_query(user_input="search the web to figure out how old dolphins can get"))