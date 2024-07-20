from FileManager import *
from ConversationManager import *
from ConsoleHelper import *
from KeyManager import *
import requests
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt

class DMI:


    def create_response(user_input="temperature, rain, wind", parameters = None, GPT_input=None):
        print_bold("Getting weather data")

        #create parameters and make api call
        parameters, times = DMI.extract_parameters(GPT_input)
        time_interval = DMI.get_time_interval(times)
        parameters = DMI.get_wanted_parameters(user_input=user_input, parameters=parameters)
        dependencies = DMI.create_dependencies(parameters=parameters, times=time_interval)
        api_data = DMI.api_call_dmi(dependencies)

        #convert the data and get the weather info
        converted_data = DMI.convert_weather_units(api_data)
        weather_list = DMI.get_weather_info(converted_data, api_data)
        # return weather_list
        filtered_weather_info = DMI.filter_weather_info(weather_list)
        
        return filtered_weather_info 
    

    def get_current_location():
        # Get the location of the user, using the ip-api to get the location of the user
        response = requests.get("http://ip-api.com/json") #("https://api.ipgeolocation.io/ipgeo?apiKey=API_KEY", "https://ipapi.co/json/", "https://ipinfo.io/json", "https://freegeoip.app/json/")
        city = response.json()["city"]
        accurate_location = response.json()["lon"], response.json()["lat"]
        return {"city": city, "accurate_location": accurate_location}
    
    def get_location_points(city="copenhagen"):
        #get long and latt from name ()
        pass
    
    def api_call_meteo():
        location = DMI.get_current_location()["accurate_location"]
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={location[0]}&longitude={location[1]}&current_weather=true")
        return response.json()

    def get_time_interval(days = None, hour = None, duration = None):        
        now = datetime.now(timezone.utc).hour + 3
        print(now)
        time_until_midnight = 24 - now

        if days == None and hour == None and (duration == None or duration == 0):
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
                    if hour == None:
                        return [0, duration]
                    
                    #duration - hour
                    start = hour-now + 24 * int(days[0])
                    return [start, start+duration]
                
                # -duration + hour
                if hour != None:
                    start = hour-now + 24 * int(days[0])
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
    

    def get_wanted_parameters(user_input = "", parameters=[]):
        # Get the wanted parameters and time interval from the user input and filter them with ChatGPT
        rain = True
        temperature = True
        wind_speed = True
        wind_dir = False
        lightnings = False
        snow = False

        if "lightning" in user_input or "thunder" in user_input:
            lightnings = True
        if "snow" in user_input or datetime.now().month in [11, 12, 1, 2, 3]: 
            snow = True
        if "wind" in user_input or "storm" in user_input:
            wind_speed = True
            wind_dir = True

        '''

        if "tomorrow" in user_input or "i morgen" in user_input:
            # get the time of today and use it to set the time interval to tomorrow morning
            now = datetime.now(timezone.utc)
            time_until_midnight = 24 - now.hour
            set_time = time_until_midnight + 6
            time = [set_time, set_time + 16]  # 6 to 22
            
        '''
        #improve to make the sorting ai-based and include location and time 


        new_parameters = []

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


    def create_dependencies(location: list = None, parameters: list = None, times: list = [0, 24]) -> dict:

        #lon  &  lat
        if location == None:
            location = DMI.get_current_location()["accurate_location"]
        else:
            location = DMI.get_location_points()

        # Format parameters for the API #https://opendatadocs.dmi.govcloud.dk/Data/Forecast_Data_Weather_Model_HARMONIE_DINI_EDR
        parameter_map = read_json_file("Dmi +\\parameter_map.json")
        tech_parameters = [parameter_map[param] for param in parameters]
        tech_parameters = ",".join(tech_parameters)
    
        # Current time and 12 hours from now and Format times for the API
        now = datetime.now(timezone.utc)  + timedelta(hours=times[0])
        future = now + timedelta(hours=times[1])
        start_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = future.strftime("%Y-%m-%dT%H:%M:%SZ")

        api_key = get_DMI_key()      

        dependencies = {        
            "coords": f"POINT({location[0]} {location[1]})",
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
        # {name: [{max: (value, time)}, {min: (value, time)}, {avg: value}, unit]}

        weather_info_list = [{"name": [{"max": ("value", "time")}, {"min": ("value", "time")}, {"avg": "value"}, "unit"]}]

        for element in cleaned_data.keys():
            name = element
            values = cleaned_data[element][0]
            max_value = round(max(values), 1)
            max_time = values.index(max_value) + hour
            min_value = round(min(values), 1)
            min_time = values.index(min_value) + hour
            avg_value = round(sum(values)/len(values), 1)
            unit = cleaned_data[element][1]
            weather_info_list.append({name: [{"max": (max_value, max_time)}, {"min": (min_value, min_time)}, {"avg": avg_value}, unit]})
        
        for element in weather_data.keys():
            if element != "temperature-2m" and element != "rain-precipitation-rate":
                name = element
                values = weather_data[element]
                max_value = round(max(values), 1)
                max_time = values.index(max_value) + hour
                min_value = round(min(values), 1)
                min_time = values.index(min_value) + hour
                avg_value = round(sum(values)/len(values), 1)
                unit = unit_map[element]
                weather_info_list.append({name: [{"max": (max_value, max_time)}, {"min": (min_value, min_time)}, {"avg": avg_value}, unit]})

        return weather_info_list
                
    def filter_weather_info(user_input, weather_info_list):
        #create a list of the wanted weather info using chatGPT
        from ChatGPT import prompt
        weather_convo = ConversationManager(promptname="weather_sort.txt").api_convo_setup(user_input=user_input, api_data=weather_info_list)
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

    print(DMI.get_time_interval(days=0, hour=None,  duration=8))

    
    parameters, time = DMI.get_wanted_parameters("temperature, rain, wind")
    api_data = DMI.api_call_dmi(DMI.create_dependencies(parameters=parameters, times=time))
    # write_json_file("Dmi +\\weather.json", api_data)
    # api_data = read_json_file("Dmi +\\weather.json")
    converted_data = DMI.convert_weather_units(api_data)
    DMI.plot_weather(converted_data)

    