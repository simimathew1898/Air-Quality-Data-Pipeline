import requests
import pandas as pd
import os
from datetime import datetime

# OpenWeatherMap API Key
API_KEY = "afc7930c8cec5aa33b9c4ec2ff59fa29"  # 🔹 Add your OpenWeatherMap API Key


# Function to get latitude & longitude
def get_lat_lon(city):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url).json()

    if not response:
        return None, None
    return response[0]["lat"], response[0]["lon"]


# Ask user for a city & validate existence
while True:
    city = input("Enter a city name: ").strip()

    lat, lon = get_lat_lon(city)
    if lat is None or lon is None:
        print(f"⚠️ Location '{city}' not found. Please enter a valid city.")
    else:
        break  # City found, proceed

print(f"📍 {city} → Latitude: {lat}, Longitude: {lon}")

# Fetch air quality data from OpenWeatherMap API
aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
aqi_response = requests.get(aqi_url).json().get("list")

if not aqi_response:
    print("⚠️ No air quality data available for this location.")
    exit()

# Extract required data
aqi_data = aqi_response[0]
air_quality = {
    "City": city,
    "Latitude": lat,
    "Longitude": lon,
    "DateTime": datetime.utcfromtimestamp(aqi_data["dt"]).strftime('%Y-%m-%d %H:%M:%S'),
    "AQI": aqi_data["main"]["aqi"],
    "CO": aqi_data["components"]["co"],
    "NO2": aqi_data["components"]["no2"],
    "O3": aqi_data["components"]["o3"],
    "SO2": aqi_data["components"]["so2"],
    "NH3": aqi_data["components"]["nh3"]
}

# Convert to Pandas DataFrame
df = pd.DataFrame([air_quality])

# 🔹 Overwrite CSV file (DO NOT append)
csv_file = "air_quality_data.csv"
df.to_csv(csv_file, mode='w', header=True, index=False)

# Print data
print("\n✅ Air Quality Data Overwritten in CSV!")
print(df.to_string(index=False))
