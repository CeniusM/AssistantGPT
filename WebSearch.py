from ChatGPT import *
from ConversationManager import *

class WebSearch:
        
    def create_response(user_input="search the web to figure out the age of dolphins"):
        #create parameters and make api call
        search_prompt = WebSearch.create_search_prompt(user_input=user_input)
        dependencies = WebSearch.create_dependencies()
        api_data = WebSearch.api_call(dependencies)

        #convert the data and get the weather info
        converted_data = WebSearch.convert_weather_units(api_data)
        weather_list = WebSearch.get_weather_info(converted_data, api_data)
        filtered_weather_info = WebSearch.filter_weather_info(weather_list)
        
        altered_user_input = user_input+"\n All the weather data available, if needed:"+filtered_weather_info
        return altered_user_input 


    def create_search_prompt(user_input):
        #create the wanted search info using chatGPT
        search_prompt_convo = ConversationManager(promptname="search_prompt.txt").api_convo_setup(user_input)
        weather_info = ChatGPT.prompt(search_prompt_convo, silent=True)