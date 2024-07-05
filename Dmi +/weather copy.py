weather = {
    "latitude": 55.57,
    "longitude": 9.7439995,
    "generationtime_ms": 0.09298324584960938,
    "utc_offset_seconds": 0,
    "timezone": "GMT",
    "timezone_abbreviation": "GMT",
    "elevation": 16.0,
    "current_weather_units": {
        "time": "iso8601",
        "interval": "seconds",
        "temperature": "\u00b0C",
        "windspeed": "km/h",
        "winddirection": "%",
        "is_day": "",
        "weathercode": "wmo code"
    },
    "current_weather": {
        "time": "2024-07-05T14:00",
        "interval": 900,
        "temperature": 13.9,
        "windspeed": 40.3,
        "winddirection": 254,
        "is_day": 1,
        "weathercode": 3
    }
}

#merge units and data
def merge_units_and_data(units, data):
    merged = {}
    for key in units:
        merged[key] = f"{data[key]} {units[key]}"
    return merged

print(merge_units_and_data(weather["current_weather_units"], weather["current_weather"]))