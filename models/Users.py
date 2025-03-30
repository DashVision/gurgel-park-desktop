import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

if os.path.exists(".env"):

    try:
        load_dotenv(".env")
        sql_password = os.getenv("SQL_PASSWORD")
    
    except:
        sql_password = ""

else:
    sql_password = ""

class UsersModel:
    def __init__(self):
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
                raise Exception("Falha na conexão com o banco de dados")
            
        except Error as e:
            print(f"Erro na conexão com o banco de dados: {e}")

        except Exception as e:
            print(f"Erro desconhecido: {e}")
            self.cursor = None

    def createUser(self, name, email, password):
        if self.cursor is None: 
            raise Exception("Não é possível criar um usuário no momento")
        
        sql_insert = f"INSERT INTO users (nome, email, senha) VALUES (%s, %s, %s)"
        values = (name, email, password)

        self.cursor.execute(sql_insert, values)
        self.connection.commit()
        return self.cursor.lastrowid
    
    def readUser(self, email, password):
        if self.cursor is None:
            raise Exception("Não é possível verificar o usuário no momento")
        
        sql_select = "SELECT * FROM users WHERE email = %s AND senha = %s"
        sql_values = (email, password)
        
        self.cursor.execute(sql_select, sql_values)
        result = self.cursor.fetchone()
        
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