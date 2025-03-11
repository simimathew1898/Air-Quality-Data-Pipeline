# Program to load data to Azure SQL

# Import libraries
import pyodbc  # Connect to SQL
import pandas as pd
from datetime import datetime

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
print("✅ Connection established")

# Create cursor to manage fetch operations
cursor = conn.cursor()

# Drop table if it exists & create a new table
cursor.execute("""
    DROP TABLE IF EXISTS AirQuality;
    CREATE TABLE AirQuality (
        id INT PRIMARY KEY IDENTITY(1,1),
        City NVARCHAR(50),
        Latitude FLOAT,
        Longitude FLOAT,
        DateTime DATETIME,
        AQI INT,
        CO FLOAT,
        NO2 FLOAT,
        O3 FLOAT,
        SO2 FLOAT,
        NH3 FLOAT
    )""")

# Save the table in the database
conn.commit()
print("✅ Table created")

# Read CSV file
df = pd.read_csv("air_quality_data.csv")

# Convert "DateTime" column from string to proper DATETIME format
df["DateTime"] = pd.to_datetime(df["DateTime"])

# Insert data into SQL
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO AirQuality (City, Latitude, Longitude, DateTime, AQI, CO, NO2, O3, SO2, NH3) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        row["City"], row["Latitude"], row["Longitude"], row["DateTime"],
        row["AQI"], row["CO"], row["NO2"], row["O3"], row["SO2"], row["NH3"]
    )

conn.commit()
print("✅ Data inserted into Azure SQL!")

# Close connection
conn.close()
