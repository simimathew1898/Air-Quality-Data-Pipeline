import requests
from datetime import datetime

API_KEY = "afc7930c8cec5aa33b9c4ec2ff59fa29"  # Replace with your OpenWeatherMap API Key

def fetch_air_quality(city):
    """Fetch air quality data from OpenWeatherMap API for a given city."""
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_response = requests.get(geo_url).json()

    print(f"\n🔍 DEBUG: API response for city '{city}': {geo_response}\n")  # ✅ Print the response

    if not isinstance(geo_response, list) or len(geo_response) == 0:
        return None, f"⚠️ City '{city}' not found. Please try again."

    # ✅ Safely get latitude & longitude
    location_data = geo_response[0]
    lat = location_data.get("lat")
    lon = location_data.get("lon")

    if lat is None or lon is None:
        return None, f"⚠️ No location data available for '{city}'."

    # Fetch air quality data
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    aqi_response = requests.get(aqi_url).json().get("list")

    print(f"\n🔍 DEBUG: Air Quality API response: {aqi_response}\n")  # ✅ Print the response

    if not isinstance(aqi_response, list) or len(aqi_response) == 0:
        return None, f"⚠️ No air quality data available for '{city}'."

    air_quality = {
        "City": city,
        "Latitude": lat,
        "Longitude": lon,
        "DateTime": datetime.utcfromtimestamp(aqi_response[0]["dt"]).strftime('%Y-%m-%d %H:%M:%S'),
        "AQI": aqi_response[0]["main"]["aqi"],
        "CO": aqi_response[0]["components"]["co"],
        "NO2": aqi_response[0]["components"]["no2"],
        "O3": aqi_response[0]["components"]["o3"],
        "SO2": aqi_response[0]["components"]["so2"],
        "NH3": aqi_response[0]["components"]["nh3"]
    }
    return air_quality, None
