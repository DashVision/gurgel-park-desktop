import os
from dotenv import load_dotenv
from mysql.connector import connect, Error

load_dotenv()

def get_connection():
    try:
        conn = connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "gurgelpark_db")
        )
        print("Conexão com o banco de dados estabelecida!")  # Log para depuração
        return conn
    
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise