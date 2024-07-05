import requests
from FileManager import *
import time
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt

class DMI:
    

    def get_location():
        # Get the location of the user
        #use the ip-api to get the location of the user
        response = requests.get("http://ip-api.com/json") #("https://api.ipgeolocation.io/ipgeo?apiKey=API_KEY", "https://ipapi.co/json/", "https://ipinfo.io/json", "https://freegeoip.app/json/")
        city = response.json()["city"]
        accurate_location = response.json()["lat"], response.json()["lon"]
        return {"city": city, "accurate_location": accurate_location}
    
    def api_call_meteo():
        location = DMI.get_location()["accurate_location"]
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={location[0]}&longitude={location[1]}&current_weather=true")
        return response.json()
    

    def create_dependencies(location: tuple = None, parameters: list = None, times: list = [0, 24]) -> dict:

        if location == None:
            location = DMI.get_location()["accurate_location"]

        if parameters == None:
            parameters =["temperature-2m", "rain-precipitation-rate", "wind-speed", "wind-dir"] #https://opendatadocs.dmi.govcloud.dk/Data/Forecast_Data_Weather_Model_HARMONIE_DINI_EDR
        # Format parameters for the API
        parameter_map = read_json_file("Dmi +\\parameter_map.json")
        tech_parameters = [parameter_map[param] for param in parameters]
        tech_parameters = ",".join(tech_parameters)
        

        # Current time and 12 hours from now and Format times for the API
        now = datetime.now(timezone.utc)  + timedelta(hours=times[0])
        future = now + timedelta(hours=times[1])
        start_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = future.strftime("%Y-%m-%dT%H:%M:%SZ")

        api_key = read_json_file("Keys\\sKey")["DMI_KEY"]        

        dependencies = {        
            "coords": f"POINT({location[1]} {location[0]})",
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

    def create_response(location, api_response):
        pass
    
    def get_weather_info(data):
        pass

    def plot_weather(data):

        #label the data
        tempatures = data["temperature-2m"] # convert from kelvin to celsius
        tempatures = [round(temp - 273.15, 8) for temp in tempatures]
        rain = data["rain-precipitation-rate"]
        rain = [rain_rate * 3.600/10 for rain_rate in rain]  # convert from Kg pr. square metres pr. second to mm pr. hour # and then divide by 10 to make the graph look better

        rain2 = [0] * len(rain)
        for time in range(1, len(rain)):         #make the rain not accumulate
            rain2[time] = round(rain[time] - rain[time-1], 8)

        wind_speed = data["wind-speed"]
        wind_dir = data["wind-dir"]
        # get the hour of now to update data
        hour = int(datetime.now(timezone.utc).hour) + 2  #2 from danish summer time
        time = range(len(tempatures))
        hours = range(hour+1, hour + len(tempatures)+1)
        hours = [h % 24 for h in hours]

        fig, ax1 = plt.subplots()
        #plot a line graph of the temperature
        color = 'tab:red'
        ax1.set_xlabel('Time (hours)')
        ax1.set_xticks(time)
        ax1.set_xticklabels(hours)
        ax1.set_ylabel('Temperature (C)', color=color)
        ax1.plot(time, tempatures, color=color, linewidth=3)
        ax1.tick_params(axis='y', labelcolor=color)


        #plot a bar graph of the rain
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Rain (mm/h)', color=color)
        ax2.bar(time, rain2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)


        if max(rain2) < 2:
            ax2.set_ylim([0, 2])
            
        ax1.set_zorder(ax2.get_zorder() + 1)  # put ax1 on top of ax2
        ax1.patch.set_visible(False)  # hide the 'spines' of ax1

        #plot the figure
        fig.tight_layout()
        plt.show()




if __name__ == "__main__":
    response = DMI.api_call_dmi(DMI.create_dependencies())
    #write_json_file("Dmi +\\weather.json", response)
    #response = read_json_file("Dmi +\\weather.json")
    DMI.plot_weather(response)

    