from Tooling.ToolConstructor import *

def get_weather_forecast_description():
    getWeather = ToolDescription("get_weather_forecast", "Get the weather forecast")
    getWeather.add_parameter_description("only fill paramereters that the user asks for. Default is rain, temperature and wind_speed set to true, and the time interval for the next 24 hours")
    
    getWeather["location"] = str, "The city"

    getWeather["rain"] = bool
    getWeather["temperature"] = bool
    getWeather["wind_speed"] = bool
    getWeather["wind_direction"] = bool
    getWeather["snow"] = bool
    getWeather["lightning"] = bool

    getWeather["day"] = str, "Enter the number of relative days, e.g. today is [0], the day after tomorrow is [2], and in four days is [4], or enter the amount of days using [start, end], so a the next week would be [0, 7]"

    getWeather["time_interval"] = int, "The amount of hours for the forecast, e.g. this evening could be interpreted as '6'"

    getWeather["time_of_day"] = int, "witch hour on the day, the interval starts, e.g. this evening would be '17'"

    return getWeather

def adjust_microphone_description():
    return ToolDescription("adjust_microphone", "Adjust the microphone for background noise")

def look_through_memory_description():
    return ToolDescription("look_through_memory", "Can look through earlier conversations. Oftenly activatet with phrases like: 'based on what we talked about' or 'do you remember?'. ")

def web_search_description():
    webSearch = ToolDescription("web_search", "Use a web query to get wanted information")

    webSearch["search_query", True] = str, "The search query that can be used for a google search, e.g. 'birth rate denmark'"

    return webSearch