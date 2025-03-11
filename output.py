import pyodbc
import pandas as pd

# Azure SQL connection credentials
SERVER = "air-quality-db.database.windows.net"
DATABASE = "air-quality"
USERNAME = "airquality"
PASSWORD = "Quality100"
DRIVER = "{ODBC Driver 18 for SQL Server}"

# Create connection string
connectionString = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

# Connect to SQL Database
conn = pyodbc.connect(connectionString)
print("\n✅ Connection established")

# Create cursor to manage fetch operations
cursor = conn.cursor()

# Run query to fetch latest data
cursor.execute(
    "SELECT City, Latitude, Longitude, DateTime, AQI, CO, NO2, O3, SO2, NH3 FROM AirQuality ORDER BY DateTime DESC")

# Fetch Results and Convert to Pandas DataFrame
columns = [column[0] for column in cursor.description]  # Get column names
rows = cursor.fetchall()  # Get data
df = pd.DataFrame.from_records(rows, columns=columns)

# Close Connection
conn.close()

# ✅ Format Output for Better Readability
if df.empty:
    print("\n⚠️ No air quality data found in the database.")
else:
    # Format DateTime
    df["DateTime"] = pd.to_datetime(df["DateTime"]).dt.strftime("%Y-%m-%d %H:%M:%S")

    # Ensure AQI is an integer
    df["AQI"] = df["AQI"].astype(int)

    # Round pollutant values to 2 decimal places
    pollutants = ["CO", "NO2", "O3", "SO2", "NH3"]
    df[pollutants] = df[pollutants].applymap(lambda x: f"{x:.2f}")


    # ✅ Categorize AQI Levels
    def categorize_aqi(aqi):
        if aqi <= 50:
            return "Good ✅"
        elif aqi <= 100:
            return "Moderate 🟡"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups 🟠"
        elif aqi <= 200:
            return "Unhealthy 🔴"
        elif aqi <= 300:
            return "Very Unhealthy 🟣"
        else:
            return "Hazardous ⚫"


    df["Air Quality Category"] = df["AQI"].apply(categorize_aqi)

    # ✅ Generate Summary Statistics
    summary = df.describe(include="all")

    # ✅ Generate Report
    report = f"""
    🌍 Air Quality Report
    --------------------------------
    ✅ Location: {df.iloc[0]['City']} (Lat: {df.iloc[0]['Latitude']}, Lon: {df.iloc[0]['Longitude']})
    📅 Report Date & Time: {df.iloc[0]['DateTime']}

    🏭 Air Quality Index (AQI): {df.iloc[0]['AQI']} ({df.iloc[0]['Air Quality Category']})

    🔬 Pollutant Levels (in µg/m³):
    - Carbon Monoxide (CO): {df.iloc[0]['CO']}
    - Nitrogen Dioxide (NO2): {df.iloc[0]['NO2']}
    - Ozone (O3): {df.iloc[0]['O3']}
    - Sulfur Dioxide (SO2): {df.iloc[0]['SO2']}
    - Ammonia (NH3): {df.iloc[0]['NH3']}


    """

    # ✅ Print Final Report
    print(report)
