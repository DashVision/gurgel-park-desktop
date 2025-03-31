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

class UsersModel:
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
                self.cursor = self.connection.cursor()
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

    def createUser(self, name, email, password):
        if self.cursor is None: 
            raise Exception("Não é possível criar um usuário no momento")
        
        sql_insert = f"INSERT INTO users (nome, email, senha) VALUES (%s, %s, %s)"
        values = (name, email, password)

        self.cursor.execute(sql_insert, values)
        self.connection.commit()
        return self.cursor.lastrowid
    
    @staticmethod
    def readUser(email, password):
        users_model = UsersModel()
        if users_model.cursor is None:
            raise Exception("Não é possível verificar o usuário no momento")
        
        sql_select = "SELECT * FROM users WHERE email = %s AND senha = %s"
        sql_values = (email, password)
        
        users_model.cursor.execute(sql_select, sql_values)
        result = users_model.cursor.fetchone()
        
        return result if result else None

    def updateUserPassword(self, email, new_password):
        if self.cursor is None:
            raise Exception("Não é possível atualizar a senha no momento")
        
        sql_update = f"UPDATE users SET senha = %s WHERE email = %s"
        sql_values = (new_password, email)
        
        self.cursor.execute(sql_update, sql_values)
        self.connection.commit()
        
        return self.cursor.lastrowid
    
    def createCar(self, car_model, car_brand, car_year):
        if self.cursor is None:
            raise Exception("Não é possível criar um novo carro neste momento")
        
        sql_insert = f"INSERT INTO cars (name, brand, year) VALUES (%s, %s, %d)"
        sql_values = (car_model, car_brand, int(car_year))

        self.cursor.execute(sql_insert, sql_values)
        self.connection.commit()

        return self.cursor.lastrowid