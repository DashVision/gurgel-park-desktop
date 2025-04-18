from config.database_config import get_connection
from models.main.vehicles import Vehicle

from typing import Optional

class VehiclesRepository:
    def __init__(self) -> None:
        print("Inicializando VehiclesRepository...")

        try:
            self.conn = get_connection()
            print("Conexão com o banco de dados estabelecida!")

        except Exception as e:
            print(f"Erro ao inicializar VehiclesRepository: {e}")
            raise

    def __del__(self) -> None:
        if self.conn.is_connected():
            print("Fechando conexão com o banco de dados...")
            self.conn.close()

    def create_vehicle(self, vehicle: Vehicle) -> None:
        print(f"Criando veículo: {vehicle}")
        cursor = self.conn.cursor()

        query = "INSERT INTO vehicles (plate, brand, model, year, color) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (vehicle.plate, vehicle.brand, vehicle.model, vehicle.year, vehicle.color))
        self.conn.commit()
        cursor.close()
        print("Veículo criado com sucesso!")

    def get_vehicle_by_credentials(self, plate: str) -> Optional[Vehicle]:
        print(f"Buscando veículo com placa: {plate}")
        cursor = self.conn.cursor()
        query = "SELECT id, plate, brand, model, year, color FROM vehicles WHERE plate = %s"
        cursor.execute(query, (plate,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            print(f"Veículo encontrado: {row}")
            vehicle = Vehicle(
                id=row[0],
                plate=row[1],
                brand=row[2],
                model=row[3],
                year=row[4],
                color=row[5]
            )
            return vehicle

        print("Nenhum veículo encontrado.")
        return None
    
    def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        print(f"Buscando veículo com ID: {vehicle_id}")
        cursor = self.conn.cursor()
        query = "SELECT id, plate, brand, model, year, color FROM vehicles WHERE id = %s"
        cursor.execute(query, (vehicle_id,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            print(f"Veículo encontrado: {row}")
            vehicle = Vehicle(
                id=row[0],
                plate=row[1],
                brand=row[2],
                model=row[3],
                year=row[4],
                color=row[5]
            )
            return vehicle

        print("Nenhum veículo encontrado.")
        return None
    
    def update_vehicle(self, vehicle: Vehicle) -> None:
        print(f"Atualizando veículo: {vehicle}")
        cursor = self.conn.cursor()

        query = "UPDATE vehicles SET plate = %s, brand = %s, model = %s, year = %s, color = %s WHERE id = %s"
        cursor.execute(query, (vehicle.plate, vehicle.brand, vehicle.model, vehicle.year, vehicle.color, vehicle.id))
        self.conn.commit()
        cursor.close()
        print("Veículo atualizado com sucesso!")

    def associate_vehicle_to_user(self, vehicle_id, user_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO vehicle_users (vehicle_id, user_id) VALUES (%s, %s)"
        cursor.execute(query, (vehicle_id, user_id))
        self.conn.commit()
        cursor.close()
        print("Veículo associado ao usuário com sucesso!")