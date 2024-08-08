from ConversationManager import *
from ConsoleHelper import *
from KeyManager import get_WEB_key
import requests

class WebSearch:
    
    def create_response(user_input=None, search_query=None):
        print_bold("Searching the web.")

        # Get search results
        if search_query is None:   
            search_query = WebSearch.create_search_query(user_input)
        dependencies = WebSearch.create_dependencies(search_query)
        search_results = WebSearch.perform_search(dependencies)

        # Format and summarize the search results
        formatted_results = WebSearch.format_results(search_results)
        filtered_search_info = WebSearch.filter_search_info(formatted_results)
        return filtered_search_info

    def create_search_query(user_input):
        search_query_convo = ConversationManager(promptname="search_query.txt").api_message_setup(user_input=user_input)
        return ChatGPT.prompt(search_query_convo)

    def create_dependencies(query, num_results=5):

        web_keys = get_WEB_key()
        api_key = web_keys[0]
        search_engine_id = web_keys[1]
        
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query,
            "num": num_results
        }
        return params
    
    def perform_search(params):
        
        url = "https://customsearch.googleapis.com/customsearch/v1"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            print(f"Error: {response.status_code}")
            return None

    def format_results(search_results):
        formatted_results = []
        for item in search_results:
            formatted_results.append({
                'title': item['title'],
                'snippet': item['snippet']
            })
        return formatted_results

    def filter_search_info(formatted_results):
        filter_search_convo = ConversationManager(promptname="filter_search.txt").api_convo_setup(api_data=formatted_results)
        return ChatGPT.prompt(filter_search_convo)

if __name__ == "__main__":
    conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "search the web to figure out if Joe Biden is still running for president"}
    ]
    set_global_conversation_manager().conversation = conversation_history
    print(WebSearch.create_response(user_input="search the web to figure out if Joe Biden is still running for president"))