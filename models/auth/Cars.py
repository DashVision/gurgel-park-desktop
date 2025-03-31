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

class CarsModel:
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

    def createCar(self, car_model, car_brand, car_year):
        if self.cursor is None:
            raise Exception("Não é possível criar um novo carro neste momento")
        
        sql_insert = f"INSERT INTO cars (name, brand, year) VALUES (%s, %s, %d)"
        sql_values = (car_model, car_brand, int(car_year))

        self.cursor.execute(sql_insert, sql_values)
        self.connection.commit()

        return self.cursor.lastrowid