from FileManager import *
from ConversationManager import *
from ConsoleHelper import *
from KeyManager import *
import requests
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt

class DMI:


    def create_response(GPT_parameters=None):
        print_bold("Getting weather data")

        #create parameters and make api call
        times, location, parameters = DMI.extract_parameters(GPT_parameters)
        time_interval = DMI.get_time_interval(times)
        location_points = DMI.get_location_points(location)
        forecast_parameters = DMI.get_wanted_parameters(parameters)
        
        dependencies = DMI.create_dependencies(times=time_interval, location_points=location_points, parameters=forecast_parameters)
        api_data = DMI.api_call_dmi(dependencies)

        #convert the data and get the weather info
        converted_data = DMI.convert_weather_units(api_data)
        weather_list = DMI.get_weather_info(converted_data, api_data)
        # return weather_list
        filtered_weather_info = DMI.filter_weather_info(weather_list)
        
        return filtered_weather_info 
    
    def api_call_meteo(): #super simple api call
        location = DMI.get_current_location()["accurate_location"]
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={location[1]}&longitude={location[0]}&current_weather=true")
        return response.json()

    def extract_parameters(GPT_parameters):
        
        #Default everything
        day, time_of_day, time_interval = None, None, None
        location = None
        rain, temperature, wind_speed, wind_direction, lightning, snow = True, True, True, False, False, False

        if GPT_parameters == None:
            times = [day, time_of_day, time_interval]
            parameters = [rain, temperature, wind_speed, wind_direction, lightning, snow] 
            return times, location, parameters

        location = GPT_parameters.get("location")

        rain = GPT_parameters.get("rain")
        temperature = GPT_parameters.get("temperature")
        wind_speed = GPT_parameters.get("wind_speed" )
        wind_direction = GPT_parameters.get("wind_direction" )
        snow = GPT_parameters.get("snow")
        lightning = GPT_parameters.get("lightning")
        
        day = GPT_parameters.get("day")
        time_of_day = GPT_parameters.get("time_of_day")
        time_interval = GPT_parameters.get("time_interval")


        if rain and datetime.now().month in [11, 12, 1, 2, 3]: 
            snow = True


        times = [day, time_of_day, time_interval]

        parameters = [rain, temperature, wind_speed, wind_direction, lightning, snow] 

        return times, location, parameters
    
    
    def get_current_location():
        # Get the location of the user, using the ip-api to get the location of the user
        response = requests.get("http://ip-api.com/json") #("https://api.ipgeolocation.io/ipgeo?apiKey=API_KEY", "https://ipapi.co/json/", "https://ipinfo.io/json", "https://freegeoip.app/json/")
        city = response.json()["city"]
        accurate_location = response.json()["lon"], response.json()["lat"]
        return {"city": city, "accurate_location": accurate_location}
    
    def get_location_points(city=None):
        if city == None:
            return DMI.get_current_location()["accurate_location"]

        #get long and latt from city name ()
        return DMI.get_current_location()["accurate_location"]
    

    def get_time_interval(times):        
        days, time_of_day, duration = times
        
        now = datetime.now(timezone.utc).hour + 3
        print(now)
        time_until_midnight = 24 - now

        if days == None and time_of_day == None and (duration == None or duration == 0):
            print("Error: No inputted time parameters, Couldn't get time interval setting it to the next 24 hours")
            return [0,24]

        if days == None:
            days = [0]
        elif type(days) == int:
            days = [days]
        elif type(days) == str:
            days = [int(days)]
        if len(days) == 2:
            if days[0] == days[1]:
                days = [0]

        try:
            #if one day is given
            if len(days) == 1:
                
                if duration != None and duration != 0:

                    #duration + hour
                    if time_of_day == None:
                        return [0, duration]
                    
                    #duration - hour
                    start = time_of_day-now + 24 * int(days[0])
                    return [start, start+duration]
                
                # -duration + hour
                if time_of_day != None:
                    start = time_of_day-now + 24 * int(days[0])
                    return [start, start+8]

            # -duration - hour
                start = time_until_midnight + 24*days[0]
                return [start, start+24]
            
            
            if len(days) == 2:
                start = time_until_midnight + 24*days[0]
                end = time_until_midnight + 24*days[1]
                return[start, end]
            
        except:
            print("Time interval wasn't formatted correctly")
        print("Couldn't get time interval setting it to the next 24 hours")
        return [0,24]
    

    def get_wanted_parameters(parameters=[]):
        # Get the wanted parameters and time interval from the user input and filter them with ChatGPT
        rain = True
        temperature = True
        wind_speed = True
        wind_dir = False
        lightnings = False
        snow = False

        new_parameters = [] # find more in DMI + folder 

        if rain:
            new_parameters.append("rain-precipitation-rate")
        if temperature:
            new_parameters.append("temperature-2m")
        if wind_speed:
            new_parameters.append("wind-speed")
        if wind_dir:
            new_parameters.append("wind-dir")
        if lightnings:
            new_parameters.append("probability-of-lightning")
        if snow:
            new_parameters.append("total-snowfall-rate-water-equivalent")

        return new_parameters


    def create_dependencies(times: list, location_points: list, parameters: list) -> dict:
    
        # Current time and 12 hours from now and Format times for the API
        now = datetime.now(timezone.utc)  + timedelta(hours=times[0])
        future = now + timedelta(hours=times[1])
        start_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = future.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Format parameters for the API #https://opendatadocs.dmi.govcloud.dk/Data/Forecast_Data_Weather_Model_HARMONIE_DINI_EDR
        parameter_map = read_json_file("Dmi +\\parameter_map.json")
        tech_parameters = [parameter_map[param] for param in parameters]
        tech_parameters = ",".join(tech_parameters)

        api_key = get_DMI_key()      

        dependencies = {        
            "coords": f"POINT({location_points[0]} {location_points[1]})",
            "crs": "crs84",
            "parameter-name": f"{tech_parameters}",
            "datetime": f"{start_time}/{end_time}",
            "api-key": f"{api_key}" 
        }
        
        return dependencies
         

    def api_call_dmi(dependencies):
        # API endpoint https://opendatadocs.dmi.govcloud.dk/APIs/Forecast_Data_EDR_API
        url = "https://dmigw.govcloud.dk/v1/forecastedr/collections/harmonie_dini_sf/position/"        

        # Make the GET request
        response = requests.get(url, params=dependencies)

        def get_parameter_data(parameter_name, data):
            if parameter_name in data['ranges']:
                return data['ranges'][parameter_name]['values']
            
        # Check if the request was successful
        if response.status_code == 200:

            tech_parameter_map = read_json_file("Dmi +\\tech_parameter_map.json")
            weather_data = {}
            for parameter in response.json()['ranges']:
                param_name = tech_parameter_map[parameter]
                weather_data[param_name] = get_parameter_data(parameter, response.json())

            return weather_data

        else:
            print(f"Error with DMI.api code: {response.status_code}\n", response.text)

    def convert_weather_units(data):
        
        #label the data
        temperatures = data["temperature-2m"] # convert from kelvin to celsius
        temperatures = [round(temp - 273.15, 8) for temp in temperatures]
        
        rain_acc = data["rain-precipitation-rate"]
        rain_acc = [rain_rate * 3.600/10 for rain_rate in rain_acc]  # convert from Kg pr. square metres pr. second to mm pr. hour # and then divide by 10 to make the graph look better

        rain = [0] * len(rain_acc)
        for time in range(1, len(rain_acc)):         #make the rain not accumulate
            rain[time] = round(rain_acc[time] - rain_acc[time-1], 8)

        # get the hour of now to update data
        hour = int(datetime.now(timezone.utc).hour) + 2  #2 from danish summer time
        hours = range(hour+1, hour + len(temperatures)+1)
        hours = [h % 24 for h in hours]

        return temperatures, rain, hour, hours

    def get_weather_info(converted_data, weather_data):
        temperatures, rain, hour, hours = converted_data
        cleaned_data = {"temperature": (temperatures, "C"), "rain": (rain, "mm/h")}
        unit_map = read_json_file("Dmi +\\parameter_unit_map.json")

        #go through the data and get the weather info 

        weather_info_list = [{"name": [{"max": ("value", "time")}, {"min": ("value", "time")}, {"avg": "value"}, "unit"]}]

        for element in cleaned_data.keys():
            name = element
            values = cleaned_data[element][0]
            max_value =max(values)
            max_time = values.index(max_value) + hour
            min_value =min(values)
            min_time = values.index(min_value) + hour
            avg_value = sum(values)/len(values)
            unit = cleaned_data[element][1]
            weather_info_list.append({name: [{"max": (round(max_value,1), round(max_time,1))}, {"min": (round(min_value,1), round(min_time,1))}, {"avg": round(avg_value,1)}, unit]})

        
        for element in weather_data.keys():
            if element != "temperature-2m" and element != "rain-precipitation-rate":
                name = element
                values = weather_data[element]
                max_value =max(values)
                max_time = values.index(max_value) + hour
                min_value =min(values)
                min_time = values.index(min_value) + hour
                avg_value = sum(values)/len(values)
                unit = unit_map[element]
                weather_info_list.append({name: [{"max": (round(max_value,1), round(max_time,1))}, {"min": (round(min_value,1), round(min_time,1))}, {"avg": round(avg_value,1)}, unit]})

        return weather_info_list
                
    def filter_weather_info(weather_info_list):
        #create a list of the wanted weather info using chatGPT

        conversation_history = [ #for now - debug
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What will the wind be like from tomorrow morning at 8 to 12 hours later in Bork Havn?"}
        ]

        weather_convo = ConversationManager(promptname="weather_sort.txt").api_convo_setup(conversation=conversation_history, api_data=weather_info_list)
        weather_info = ChatGPT.prompt(weather_convo)

        return weather_info



    def plot_weather(data):

        temperatures, rain, hour, hours = data
        time = range(len(temperatures))

        fig, ax1 = plt.subplots()
        #plot a line graph of the temperature
        color = 'tab:red'
        ax1.set_xlabel('Time (hour)')
        ax1.set_xticks(time)
        ax1.set_xticklabels(hours)
        ax1.set_ylabel('Temperature (C)', color=color)
        ax1.plot(time, temperatures, color=color, linewidth=3)
        ax1.tick_params(axis='y', labelcolor=color)


        #plot a bar graph of the rain
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Rain (mm/h)', color=color)
        ax2.bar(time, rain, color=color)
        ax2.tick_params(axis='y', labelcolor=color)


        if max(rain) < 2:
            ax2.set_ylim([0, 2])
            
        ax1.set_zorder(ax2.get_zorder() + 1)  # put ax1 on top of ax2
        ax1.patch.set_visible(False)  # hide the 'spines' of ax1

        #plot the figure
        fig.tight_layout()
        plt.show()
                            

if __name__ == "__main__":

    print(DMI.get_current_location())
    print(DMI.get_time_interval(["1", 8, 12]))

    
    parameters, time = DMI.get_wanted_parameters("temperature, rain, wind")
    api_data = DMI.api_call_dmi(DMI.create_dependencies(parameters=parameters, times=time))
    # write_json_file("Dmi +\\weather.json", api_data)
    # api_data = read_json_file("Dmi +\\weather.json")
    converted_data = DMI.convert_weather_units(api_data)
    DMI.plot_weather(converted_data)

    