import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER").strip()
SQL_DATABASE = os.getenv("SQL_DATABASE").strip()
SQL_DRIVER = os.getenv("SQL_DRIVER").strip()
UID = os.getenv("SQL_USER").strip()
PWD = os.getenv("SQL_PASSWORD").strip()

# Defina a sua string de conexão segura
CONN_STR = (
    f"Driver={SQL_DRIVER};"
    f"Server=tcp:{SQL_SERVER},1433;"
    f"Database={SQL_DATABASE};"
    f"Encrypt=no;"
    f"UID={UID};"
    f"PWD={PWD};"
    f"Connection Timeout=30;"
)

with pyodbc.connect(CONN_STR) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'")
    tables = [row[0] for row in cursor.fetchall()]

    print(tables)