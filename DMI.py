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
        
        # filter relevant weather info
        filtered_weather_info = DMI.filter_weather_info(weather_list)
        return filtered_weather_info 
    
    def api_call_meteo(): #super simple api call
        location = DMI.get_current_location()["accurate_location"]
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={location[1]}&longitude={location[0]}&current_weather=true")
        return response.json()

    def extract_parameters(GPT_parameters):
        
        #Default everything
        values = {"day": None, "time_of_day": None, "time_interval": None, "location": None, "rain": True, "temperature": True, "wind_speed": True, "wind_direction": False, "snow": False, "lightning": False}
        
        times = [values["day"], values["time_of_day"], values["time_interval"]]
        location = values["location"]
        parameters = [values["rain"], values["temperature"], values["wind_speed"], values["wind_direction"], values["lightning"], values["snow"]]

        # Check if the GPT_parameters are None and return the default values
        if GPT_parameters == None:
            return times, location, parameters
        
        # Iterate through the keys and retrieve the values with error handling
        for key in values.keys():
            try:
                key_value = GPT_parameters.get(key)
                if key_value != None:
                    values[key] = key_value
            except:
                pass

        #check snow
        if values["rain"] == True and datetime.now().month in [11, 12, 1, 2, 3]:
            values["snow"] = True

        #create bundles
        times = [values["day"], values["time_of_day"], values["time_interval"]]
        location = values["location"]
        parameters = [values["rain"], values["temperature"], values["wind_speed"], values["wind_direction"], values["lightning"], values["snow"]]

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

        if days == None and time_of_day == None and (duration == None or duration == 0):
            print("Error: No inputted time parameters, Couldn't get time interval setting it to the next 24 hours")
            return [0,24]
        
        now = (datetime.now(timezone.utc).hour + 3) % 24 #3 from danish summer time 
        time_until_midnight = (24 - now) % 24

        if time_of_day != None:
            time_from_now = (time_of_day - now) % 24


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
                    start = time_from_now + 24 * int(days[0])
                    return [start, start+duration]
                
                # -duration + hour
                if time_of_day != None:
                    start = time_from_now + 24 * int(days[0])
                    return [start, start+8]

                if days[0] == 0:
                    return [0, time_until_midnight]
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
    

    def get_wanted_parameters(parameters):
        rain, temperature, wind_speed, wind_direction, lightnings, snow = parameters

        parameter_map = { # find more in DMI + folder 
            "rain-precipitation-rate": rain, 
            "temperature-2m": temperature,
            "wind-speed": wind_speed,
            "wind-dir": wind_direction,
            "probability-of-lightning": lightnings,
            "total-snowfall-rate-water-equivalent": snow
        }

        new_parameters = []

        # Iterate over the dictionary and add parameters based on their condition
        for param, condition in parameter_map.items():
            if condition:
                new_parameters.append(param)

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
        hour = int(datetime.now(timezone.utc).hour) + 4  #3 from danish summer time 1 from 
        hours = range(hour+1, hour + len(temperatures)+1)
        hours = [h % 24 for h in hours]

        return temperatures, rain, hour, hours

    def get_weather_info(converted_data, weather_data):
        now = datetime.now(timezone.utc).hour + 4
        temperatures, rain, hour, hours = converted_data
        cleaned_data = {"temperature": (temperatures, "C"), "rain": (rain, "mm/h")}
        unit_map = read_json_file("Dmi +\\parameter_unit_map.json")

        #go through the data and get the weather info 

        weather_info_list = [{"name": [{"max": ("value", "time")}, {"min": ("value", "time")}, {"avg": "value"}, "unit"]}]

        for element in cleaned_data.keys():
            name = element
            values = cleaned_data[element][0]
            max_value =max(values)
            max_time = (values.index(max_value) + hour) % 24
            min_value =min(values)
            min_time = (values.index(min_value) + hour) % 24
            avg_value = sum(values)/len(values)
            unit = cleaned_data[element][1]
            weather_info_list.append({name: [{"max": (round(max_value,1), round(max_time,1))}, {"min": (round(min_value,1), round(min_time,1))}, {"avg": round(avg_value,1)}, unit]})

        
        for element in weather_data.keys():
            if element != "temperature-2m" and element != "rain-precipitation-rate":
                name = element
                values = weather_data[element]
                max_value =max(values)
                max_time = (values.index(max_value) + hour) % 24
                min_value =min(values)
                min_time = (values.index(min_value) + hour) % 24
                avg_value = sum(values)/len(values)
                unit = unit_map[element]
                weather_info_list.append({name: [{"max": (round(max_value,1), round(max_time,1))}, {"min": (round(min_value,1), round(min_time,1))}, {"avg": round(avg_value,1)}, unit]})

        return weather_info_list
                
    def filter_weather_info(weather_info_list):
        #create a list of the wanted weather info using chatGPT
        weather_convo = ConversationManager(promptname="weather_sort.txt").api_convo_setup(api_data=weather_info_list)
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

    # print(DMI.create_response({'temperature': True, 'rain': True, 'wind_speed': True, 'time_interval': 5}))
    # print(DMI.get_time_interval([0, 1, None]))
    
    times, location, parameters = DMI.extract_parameters({'temperature': True, 'rain': True, 'wind_speed': True, 'time_interval': 35})
    time_interval = DMI.get_time_interval(times)
    location_points = DMI.get_location_points(location)
    forecast_parameters = DMI.get_wanted_parameters(parameters)
    
    dependencies = DMI.create_dependencies(times=time_interval, location_points=location_points, parameters=forecast_parameters)
    api_data = DMI.api_call_dmi(dependencies)
    converted_data = DMI.convert_weather_units(api_data)
    DMI.plot_weather(converted_data)

    weather_list = DMI.get_weather_info(converted_data, api_data)
    filtered_weather_info = DMI.filter_weather_info(weather_list)
    print(filtered_weather_info)
    

    

    