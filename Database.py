import pyodbc

class DB:
    server = 'localhost'
    database = 'Training'
    port = '1433'

    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
    )

    try:
        conn = pyodbc.connect(conn_str)
        print("Connected to the database successfully")
    except Exception as e:
        print("Error connecting to the database:", e)