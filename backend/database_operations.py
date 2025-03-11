import pyodbc
import pandas as pd
from database_config import get_db_connection


def save_to_database(data):
    """Saves air quality data to Azure SQL."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO AirQuality (City, Latitude, Longitude, DateTime, AQI, CO, NO2, O3, SO2, NH3)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data["City"], data["Latitude"], data["Longitude"], data["DateTime"], data["AQI"],
                   data["CO"], data["NO2"], data["O3"], data["SO2"], data["NH3"])

    conn.commit()
    conn.close()


def get_air_quality_data_from_db():
    """Retrieves air quality data from Azure SQL."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM AirQuality ORDER BY DateTime DESC")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame.from_records(rows, columns=columns)
    return df.to_dict(orient="records")
