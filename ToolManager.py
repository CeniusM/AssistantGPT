from Tooling.Tool import *

# Tools
from DMI import *
from Memory import *
from WebSearch import *
from SmartMic import *
from NoteTool import *

# Returns a dict of the avalible tools. It include the names, tool description and function to be called
def get_available_tools():

    # Defines all the tools that the GPT agent can use
    tools = [
        Tool(
            name = "get_weather_forecast",
            description = "Get the weather forecast",
            args_description = "only fill paramereters that the user asks for. Default is rain, temperature and wind_speed set to true, and the time interval for the next 24 hours",
            args = [
                ToolArg("location", str).describe("The city"),
                ToolArg("rain", bool),
                ToolArg("temperature", bool),
                ToolArg("wind_speed", bool),
                ToolArg("wind_direction", bool),
                ToolArg("snow", bool),
                ToolArg("lightning", bool),
                ToolArg("day", str).describe("Enter the number of relative days, e.g. today is [0], the day after tomorrow is [2], and in four days is [4], or enter the amount of days using [start, end], so a the next week would be [0, 7]"),
                ToolArg("time_interval", int).describe("The amount of hours for the forecast, e.g. this evening could be interpreted as '6'"),
                ToolArg("time_of_day", int).describe("witch hour on the day, the interval starts, e.g. this evening would be '17'")
            ],
            function_call = DMI.create_response
        ),
        Tool(
            name = "adjust_microphone",
            description = "Adjust the microphone for background noise",
            function_call = lambda: SmartMic(),
            default_response = "Microphone adjusted"
        ),
        Tool(
            name = "look_through_memory",
            description = "Can look through earlier conversations. Oftenly activatet with phrases like: 'based on what we talked about' or 'do you remember?'. ",
            function_call = Memory.create_response
        ),
        Tool(
            name = "web_search",
            description = "Use a web query to get wanted information",
            args = [
                ToolArg("search_query", str).required().describe("The search query that can be used for a google search, e.g. 'birth rate denmark'")
            ],
            function_call = WebSearch.create_response
        ),
        Tool(
            name = "make_note",
            description = "Makes a note with a title and some contents. The tool will return Succes, then title and content, or Failed with an error message if the note title allready exsists",
            args_description = "Here are some arguments",
            args = [
                ToolArg("title").required(),
                ToolArg("content").required()
            ],
            function_call = NoteTools.make_note
        )
    ]
    
    return tools, [a.__dict__() for a in tools]