import pyodbc


def get_db_connection():
    SERVER = "air-quality-db.database.windows.net"
    DATABASE = "air-quality"
    USERNAME = "airquality"
    PASSWORD = "Quality100"
    DRIVER = "{ODBC Driver 18 for SQL Server}"

    return pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')
