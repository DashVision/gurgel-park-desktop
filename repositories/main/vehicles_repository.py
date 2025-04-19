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

    def create_vehicle(self, vehicle: Vehicle) -> int:
        print(f"Criando veículo: {vehicle}")
        cursor = self.conn.cursor()

        query = """
            INSERT INTO vehicles (placa, marca, modelo, ano, cor, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (vehicle.plate, vehicle.brand, vehicle.model, vehicle.year, vehicle.color, vehicle.user_id))
        self.conn.commit()
        vehicle_id = cursor.lastrowid
        cursor.close()
        print("Veículo criado com sucesso!")
        return vehicle_id

    def get_vehicle_by_credentials(self, placa):
        cursor = self.conn.cursor()
        query = "SELECT id, placa, marca, modelo, ano, cor, user_id FROM vehicles WHERE placa = %s"
        cursor.execute(query, (placa,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            # Retorna um dicionário com os dados do veículo
            return {
                "id": result[0],
                "placa": result[1],
                "marca": result[2],
                "modelo": result[3],
                "ano": result[4],
                "cor": result[5],
                "user_id": result[6],
            }
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
    
    def get_vehicles_by_user_id(self, user_id: int) -> list[Vehicle]:
        cursor = self.conn.cursor()
        query = """
            SELECT id, placa, marca, modelo, ano, cor
            FROM vehicles
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        cursor.close()

        vehicles = []
        for row in rows:
            vehicles.append(Vehicle(
                id=row[0],
                plate=row[1],
                brand=row[2],
                model=row[3],
                year=row[4],
                color=row[5]
            ))
        return vehicles
    
    def update_vehicle(self, vehicle: Vehicle) -> None:
        print(f"Atualizando veículo: {vehicle}")
        cursor = self.conn.cursor()

        query = """
            UPDATE vehicles
            SET placa = %s, marca = %s, modelo = %s, ano = %s, cor = %s
            WHERE id = %s
        """
        cursor.execute(query, (vehicle.plate, vehicle.brand, vehicle.model, vehicle.year, vehicle.color, vehicle.id))
        self.conn.commit()
        cursor.close()
        print("Veículo atualizado com sucesso!")

    def associate_vehicle_to_user(self, vehicle_id: int, user_id: int) -> None:
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO vehicle_users (vehicle_id, user_id) VALUES (%s, %s)"
            cursor.execute(query, (vehicle_id, user_id))
            self.conn.commit()
            cursor.close()
            print("Veículo associado ao usuário com sucesso!")
        except Exception as e:
            print(f"Erro ao associar veículo ao usuário: {e}")
            raise

    def delete_vehicle(self, vehicle_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM vehicles WHERE id = %s"
        cursor.execute(query, (vehicle_id,))
        self.conn.commit()
        cursor.close()
        print("Veículo deletado com sucesso!")

    def get_vehicle_by_plate(self, placa):
        cursor = self.conn.cursor()
        query = "SELECT id, placa, marca, modelo, ano, cor, user_id FROM vehicles WHERE placa = %s"
        cursor.execute(query, (placa,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            # Retorna um dicionário com os dados do veículo
            return {
                "id": result[0],
                "placa": result[1],
                "marca": result[2],
                "modelo": result[3],
                "ano": result[4],
                "cor": result[5],
                "user_id": result[6],
            }
        return None

    def get_users_by_vehicle_id(self, vehicle_id: int) -> list[int]:
        """Obtém os IDs dos usuários associados a um veículo."""
        try:
            cursor = self.conn.cursor()
            query = "SELECT user_id FROM vehicle_users WHERE vehicle_id = %s"
            cursor.execute(query, (vehicle_id,))
            rows = cursor.fetchall()
            cursor.close()
            return [row[0] for row in rows]
        except Exception as e:
            print(f"Erro ao buscar usuários associados ao veículo: {e}")
            raise

    def is_vehicle_shared_with_user(self, vehicle_id: int, user_id: int) -> bool:
        """Verifica se um veículo já está compartilhado com um usuário."""
        try:
            cursor = self.conn.cursor()
            query = "SELECT COUNT(*) FROM vehicle_users WHERE vehicle_id = %s AND user_id = %s"
            cursor.execute(query, (vehicle_id, user_id))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except Exception as e:
            print(f"Erro ao verificar compartilhamento de veículo: {e}")
            raise