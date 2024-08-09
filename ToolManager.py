from varname import nameof
from DMI import *
from Memory import *
from WebSearch import *
from SmartMic import *
from Tooling.ToolDescriptions import *

# Returns a dict of the avalible tools. It include the names, tool description and function to be called
def get_available_tools():
    tools = {
        "get_weather_forecast": {
            "description": get_weather_forecast_description(),
            "function": DMI.create_response
        },
        
        "adjust_microphone": {
            "description": adjust_microphone_description(),
            "function": SmartMic().adjust_for_ambient_noise
        },
        
        "look_through_memory": {
            "description": look_through_memory_description(),
            "function": Memory.create_response
        },
        
        "web_search": {
            "description": web_search_description(),
            "function": WebSearch.create_response
        }
    }
    
    return tools


