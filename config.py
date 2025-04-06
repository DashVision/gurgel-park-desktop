from dotenv import load_dotenv
import os

load_dotenv()

if os.path.exists(".env"):
    try:
        load_dotenv(".env")
        sql_password = os.getenv("SQL_PASSWORD")

    except:
        sql_password = ""

else:
    sql_password = ""

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sql_password',
    'database': 'gurgelpark_db'
}