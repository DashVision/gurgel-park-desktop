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

class VehicleModel:
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

    def vehicle_registrator(self, license_plate: str, brand: str, model: str, year: int, color: str, user_id: int) -> int:
        try:
            check_sql = "SELECT id FROM vehicles WHERE placa = %s"
            self.cursor.execute(check_sql, (license_plate,))
            if self.cursor.fetchone():
                raise Exception("Placa já cadastrada no sistema")

            sql_insert = "INSERT INTO vehicles (placa, marca, modelo, ano, cor, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
            sql_values = (license_plate, brand, model, year, color, user_id)

            self.cursor.execute(sql_insert, sql_values)
            self.connection.commit()

            return self.cursor.lastrowid

        except Error as e:
            print(f"Erro ao registrar veículo: {e}")
            self.connection.rollback()
            raise Exception(f"Erro ao registrar veículo: {str(e)}")

    def get_user_vehicles(self, user_id: int) -> list:
        try:
            sql_query = "SELECT * FROM vehicles WHERE user_id = %s ORDER BY created_at DESC"
            self.cursor.execute(sql_query, (user_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar veículos do usuário: {e}")
            return []

    def get_vehicle_by_id(self, vehicle_id: int, user_id: int) -> dict:
        try:
            sql_query = "SELECT * FROM vehicles WHERE id = %s AND user_id = %s"
            self.cursor.execute(sql_query, (vehicle_id, user_id))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Erro ao buscar veículo: {e}")
            return None

    def delete_vehicle(self, vehicle_id: int, user_id: int) -> bool:
        try:
            sql_query = "DELETE FROM vehicles WHERE id = %s AND user_id = %s"
            self.cursor.execute(sql_query, (vehicle_id, user_id))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Erro ao deletar veículo: {e}")
            self.connection.rollback()
            return False
            
    def get_recent_activities(self, user_id: int, limit: int = 5) -> list:
        try:
            # Verificar conexão e reconectar se necessário
            if not self.connection or not self.connection.is_connected():
                print("Reconectando ao banco de dados")
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password=sql_password,
                    database="gurgelpark_db",
                )
                self.cursor = self.connection.cursor(dictionary=True)
            
            # Verificar se a conexão é válida
            if not self.connection.is_connected():
                print("Falha na reconexão. Tentando novamente.")
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password=sql_password,
                    database="gurgelpark_db",
                )
                self.cursor = self.connection.cursor(dictionary=True)
                
            # Consulta para obter atividades recentes
            sql_query = """
                SELECT 
                    id, 
                    placa, 
                    marca, 
                    modelo, 
                    ano,
                    cor,
                    'vehicle_registration' as activity_type, 
                    created_at 
                FROM 
                    vehicles 
                WHERE 
                    user_id = %s 
                ORDER BY 
                    created_at DESC 
                LIMIT %s
            """
            
            # Executar consulta
            self.cursor.execute(sql_query, (user_id, limit))
            results = self.cursor.fetchall()
            
            # Verificar resultados
            print(f"Consulta executada. Resultados: {len(results)}")
            for vehicle in results:
                print(f"Veículo encontrado: {vehicle['marca']} {vehicle['modelo']} ({vehicle['placa']})")
                
            return results
            
        except Error as e:
            print(f"Erro ao buscar atividades recentes: {e}")
            return []
        except Exception as e:
            print(f"Exceção ao buscar atividades: {e}")
            import traceback
            traceback.print_exc()
            return []