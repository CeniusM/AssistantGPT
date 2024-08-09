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
    # tools also takes care of formatting the arguments given by the ai
    #
    # Here we just call the function
    # lambda args: Func
    #
    # Here we call the function with some args, and where they are parsed
    # lambda args: Func(args)
    # lambda args: Func(args.get("some query"))
    #
    # And here we give a predifined response
    # lambda args: (Func, "Some predifined stuff")[1]
    tools = {
        "get_weather_forecast": {
            "description": get_weather_forecast_description(),
            "function": lambda args: DMI.create_response(args)
        },
        
        "adjust_microphone": {
            "description": adjust_microphone_description(),
            # Do not need to call adjust microphone on the SmartMic since it does that after initializing
            "function": lambda args: (SmartMic(), "Microphone adjusted")[1]
        },
        
        "look_through_memory": {
            "description": look_through_memory_description(),
            "function": lambda args: Memory.create_response
        },
        
        "web_search": {
            "description": web_search_description(),
            "function": lambda args: WebSearch.create_response(args.get("search_query"))
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
