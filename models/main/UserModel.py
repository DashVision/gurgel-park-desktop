import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

if os.path.exists(".env"):
    try:
        load_dotenv(".env")
        sql_password = os.getenv("SQL_PASSWORD")

        if not sql_password:
            print("Aviso: SQL_PASSWORD não está definido no arquivo .env")

    except Exception as e:
        print(f"Erro ao carregar .env: {e}")
        sql_password = ""
        
else:
    print("Arquivo .env não encontrado.")
    sql_password = ""

class UserModel:
    def __init__(self):
        self.connection = None 
        self.cursor = None      

        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=sql_password,
                database="gurgelpark_db",
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Conexão bem sucedida com o banco de dados")

            else:
                print("Falha na conexão: banco de dados não conectado.")

        except Error as e:
            print(f"Erro na conexão com o banco de dados: {e}")
            self.connection = None
            self.cursor = None

        except Exception as e:
            print(f"Erro desconhecido: {e}")
            self.connection = None
            self.cursor = None
    
    def get_user_data(self, email):
        if self.cursor is None:
            raise Exception("Não é possível obter dados do usuário no momento")
        
        sql_select = "SELECT id, nome, email FROM users WHERE email = %s"
        values = (email,)
        
        self.cursor.execute(sql_select, values)
        result = self.cursor.fetchone()
        
        return result if result else None
        
    def __del__(self):
        if hasattr(self, 'connection') and self.connection is not None:
            if hasattr(self, 'cursor') and self.cursor is not None:
                self.cursor.close()
            self.connection.close() 