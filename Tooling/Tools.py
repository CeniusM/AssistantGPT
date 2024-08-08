from ToolConstructor import *

def testing():

    # getWeather = ToolDescription(
    #     name="get_weather_forecast",
    #     description="Get the weather forecast")
    
    # # getWeather.add_parameters(
    # #     description="description"
    # #     arguments=
    # #     [
    # #         { "rain", bool }
    # #         { "temperature", bool }
    # #         { "wind_speed", bool }
    # #         { "wind_direction", bool }
    # #         { "snow", bool }
    # #         { "lightning", bool }
    # #     ]
    # # )
    
    # getWeather.add_parameter_description(
    #     "only fill paramereters that the user asks for. Default is rain, temperature and wind_speed set to true, and the time interval for the next 24 hours")

    # getWeather.add_parameter(
    #     "location",
    #     str)
    
    # getWeather.add_parameter("rain", bool)
    # getWeather.add_parameter("temperature", bool)
    # getWeather.add_parameter("wind_speed", bool)
    # getWeather.add_parameter("wind_direction", bool)
    # getWeather.add_parameter("snow", bool)
    # getWeather.add_parameter("lightning", bool)

    # getWeather.add_parameter(
    #     "day", 
    #     str, 
    #     "Enter the number of relative days, e.g. today is [0], the day after tomorrow is [2], and in four days is [4], or enter the amount of days using [start, end], so a the next week would be [0, 7]")

    # getWeather.add_parameter(
    #     "time_interval",
    #     str,
    #     "The amount of hours for the forecast, e.g. this evening could be interpreted as '6'")
    
    # getWeather.add_parameter(
    #     "time_of_day",
    #     str,
    #     "Enter the number of relative days, e.g. today is [0], the day after tomorrow is [2], and in four days is [4], or enter the amount of days using [start, end], so a the next week would be [0, 7]")

    

    volumeTool = ToolDescription("volume", "Changes the pc volume")
    
    volumeTool.add_parameter("amplitude", int, "number from 0 to 100")


    print("yoyo")