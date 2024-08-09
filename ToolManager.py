from varname import nameof
from DMI import *
from Memory import *
from WebSearch import *
from SmartMic import *
from Tooling.Tools import *

# Returns a dict of the avalible tools. It include the names, tool description and function to be called
def get_available_tools():
    tools = {
        nameof(get_weather): {
            "description": get_weather_forecast_description(),
            "func": get_weather
        },
        
        nameof(look_through_memory): {
            "description": look_through_memory_description(),
            "func": look_through_memory
        },
        
        nameof(web_search): {
            "description": web_search_description(),
            "func": web_search
        },
        
        nameof(adjust_mic): {
            "description": adjust_microphone_description(),
            "func": adjust_mic
        }
    }
    
    return tools

def get_weather(GPT_parameters):
    return DMI.create_response(GPT_parameters)


def look_through_memory():
    return Memory.create_response()

def web_search(search_query):
    return WebSearch.create_response(search_query=search_query)
    
def adjust_mic():
    SmartMic().adjust_for_ambient_noise()

