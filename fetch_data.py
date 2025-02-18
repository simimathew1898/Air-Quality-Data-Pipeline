# Program to fetch real-time air quality air data
from http.client import responses

# Import packages
import requests  # It is used to fetch data from an API
import pandas as pd # It is used for handling data

# Fetching data from Openweathermap API
LAT , LON = 34.4248, 150.8931
API_KEY = "afc7930c8cec5aa33b9c4ec2ff59fa29"

url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

# Sending API request and retrieving the data in json
response = requests.get(url)
data = response.json()
print(data)

# Extracting the data
air_quality_data = []
for item in data["list"]:
    air_quality_data.append({
        "dt": item["dt"], # Date and time
        "aqi": item["main"]["aqi"], # Air Quality Index
        "co": item["components"]["co"], # Сoncentration of CO (Carbon monoxide)
        "no2": item["components"]["no2"], # Сoncentration of NO2(Nitrogen dioxide)
        "o3": item["components"]["o3"], # Сoncentration of O3 (Ozone)
        "so2": item["components"]["so2"], # Сoncentration of SO2 (Sulphur dioxide)
        "nh3": item["components"]["nh3"] #  Сoncentration of NH3 (Ammonia)
    })
print(air_quality_data)

# Converting to dataframe and saving it as CSV file
df = pd.DataFrame(air_quality_data) # Conversion to dataframe
df.to_csv("air_quality_data.csv", index=False) #Saving it as csv, index=False to prevent pandas to add an extra column for row number
print("Data saved into air_quality_data.csv")
