import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class VehiclesMain:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor(dictionary=True)

    def vehicle_registrator(self, license_plate: str, brand: str, model: str, year: int, color: str, user_id: int) -> int:
        try:
            check_sql = "SELECT id FROM vehicles WHERE placa = %s"
            self.cursor.execute(check_sql, (license_plate,))
            if self.cursor.fetchone():
                raise Exception("Placa j� cadastrada no sistema")

            sql_insert = "INSERT INTO vehicles (placa, marca, modelo, ano, cor, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
            sql_values = (license_plate, brand, model, year, color, user_id)

            self.cursor.execute(sql_insert, sql_values)
            self.connection.commit()

            return self.cursor.lastrowid

        except Error as e:
            print(f"Erro ao registrar ve�culo: {e}")
            self.connection.rollback()
            raise Exception(f"Erro ao registrar ve�culo: {str(e)}")

    def get_user_vehicles(self, user_id: int) -> list:
        try:
            sql_query = "SELECT * FROM vehicles WHERE user_id = %s ORDER BY created_at DESC"
            self.cursor.execute(sql_query, (user_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar ve�culos do usu�rio: {e}")
            return []

    def get_vehicle_by_id(self, vehicle_id: int, user_id: int) -> dict:
        try:
            sql_query = "SELECT * FROM vehicles WHERE id = %s AND user_id = %s"
            self.cursor.execute(sql_query, (vehicle_id, user_id))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Erro ao buscar ve�culo: {e}")
            return None

    def delete_vehicle(self, vehicle_id: int, user_id: int) -> bool:
        try:
            sql_query = "DELETE FROM vehicles WHERE id = %s AND user_id = %s"
            self.cursor.execute(sql_query, (vehicle_id, user_id))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Erro ao deletar ve�culo: {e}")
            self.connection.rollback()
            return False
            
    def get_recent_activities(self, user_id: int, limit: int = 5) -> list:
        try:
            if not self.connection or not self.connection.is_connected():
                print("Reconectando ao banco de dados")
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="gurgelpark_db",
                )
                self.cursor = self.connection.cursor(dictionary=True)
            
            # Verificar se a conex�o � v�lida
            if not self.connection.is_connected():
                print("Falha na reconex�o. Tentando novamente.")
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
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
            
            self.cursor.execute(sql_query, (user_id, limit))
            results = self.cursor.fetchall()
            
            # Verificar resultados
            print(f"Consulta executada. Resultados: {len(results)}")
            for vehicle in results:
                print(f"Ve�culo encontrado: {vehicle['marca']} {vehicle['modelo']} ({vehicle['placa']})")
                
            return results
            
        except Error as e:
            print(f"Erro ao buscar atividades recentes: {e}")
            return []

        except Exception as e:
            print(f"Exce��o ao buscar atividades: {e}")
            import traceback
            traceback.print_exc()
            return []
