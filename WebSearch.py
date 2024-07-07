from ChatGPT import *
from ConversationManager import *

class WebSearch:
        
    def create_response(user_input="search the web to figure out the age of dolphins"):
        #create parameters and make api call
        search_query = WebSearch.create_search_query(user_input=user_input)
        dependencies = WebSearch.create_dependencies()
        api_data = WebSearch.api_call(dependencies)

        #convert the data from the search
        converted_data = WebSearch.convert_api_data(api_data)
        search_info = WebSearch.manage_data(converted_data)
        
        altered_user_input = user_input+"\n Search info, if needed: "+search_info
        return altered_user_input 


    def create_search_query(user_input):
        #create the wanted search info using chatGPT
        search_query_convo = ConversationManager(promptname="search_query.txt").api_convo_setup(user_input)
        search_query = ChatGPT.prompt(search_query_convo, silent=True)
        return search_query


if __name__ == "__main__":
    print(WebSearch.create_search_query("search the web to figure out the age of dolphins"))