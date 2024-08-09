from varname import nameof
from DMI import *
from Memory import *
from WebSearch import *
from SmartMic import *
from Tooling.ToolDescriptions import *

# Returns a dict of the avalible tools. It include the names, tool description and function to be called
def get_available_tools():

    # here we define our tools, each tool has a name.
    # then it has a description defined in ToolDescriptions.py
    # there we define the parameters and further descriptions
    #
    # tools also defines some formatting of the arguments given by the ai
    tools = {
        "get_weather_forecast": {
            "description": get_weather_forecast_description(),
            "function": DMI.create_response,
            "use_args": True,
        },
        
        "adjust_microphone": {
            "description": adjust_microphone_description(),
            # Do not need to call adjust microphone on the SmartMic since it does that after initializing
            "function": lambda: SmartMic(),
            "use_args": False,
            "response": "Microphone adjusted"
        },
        
        "look_through_memory": {
            "description": look_through_memory_description(),
            "function": Memory.create_response,
            "use_args": False,
        },
        
        "web_search": {
            "description": web_search_description(),
            "function": WebSearch.create_response,
            "use_args": True,
            "get": "search_query"
        }
    }
    
    return tools

def get_available_tools_json():
    # get tools
    tools = get_available_tools()
    # get each tool json
    tools_for_json = [tools[t]["description"].to_json() for t in tools]
    # combines with "," and adds [] around
    return json.loads(f"[{str.join(",\n",tools_for_json)}]")
