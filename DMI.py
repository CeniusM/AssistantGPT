import requests
from FileManager import *
import time
from datetime import datetime, timedelta, timezone

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
    
    def api_call_dmi(location=None, times=[0, 12], parameters=None):
        # API endpoint https://opendatadocs.dmi.govcloud.dk/APIs/Forecast_Data_EDR_API
        url = "https://dmigw.govcloud.dk/v1/forecastedr/collections/harmonie_dini_sf/position"        
        headers = {"X-Gravitee-Api-Key": "c56a6d83-46a3-4482-b875-8ca18bdd56c7"}
        
        if location == None:
            location = DMI.get_location()["accurate_location"]

        if parameters == None:
            parameters = ["temperature-2m", "wind-speed-10m", "wind-dir-10m"]

        # Current time and 12 hours from now and Format times for the API
        now = datetime.now(timezone.utc)  + timedelta(hours=times[0])
        future = now + timedelta(hours=times[1])
        start_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time = future.strftime("%Y-%m-%dT%H:%M:%SZ")

        api_key = read_json_file("Keys\\sKey")["DMI_KEY"]        

        params = {         # Parameters
            "coords": f"POINT({location[1]} {location[0]})",
            "crs": "crs84",
            "parameter-name": f"{parameters}",
            "datetime": f"{start_time}/{end_time}",
            "api-key": f"{api_key}"
        }

        # Make the GET request
        response = requests.get(url, params=params, headers=headers)
        print(response, response.text)
        write_json_file("Dmi\\weather.json", response.json())

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Process and print the data
            for feature in data['features']:
                step = feature['properties']['step']
                temp = feature['properties']['temperature-2m']
                wind_speed = feature['properties']['wind-speed-10m']
                wind_dir = feature['properties']['wind-dir-10m']
                print(f"Time: {step}, Temp: {temp}K, Wind Speed: {wind_speed}m/s, Wind Direction: {wind_dir}°")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

        
        


    def create_response(location, api_response):
        pass
    
    def get_weather():
        pass


if __name__ == "__main__":
    write_json_file("Dmi\\weather.json2", DMI.api_call_dmi())
    