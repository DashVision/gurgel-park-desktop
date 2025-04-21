from core.config.database_config import get_connection

class ParkingRepository:
    def __init__(self):
        self.conn = get_connection()

    def create_parking_configuration(self, establishment_id, rows, columns, spot_type):
        """Cria uma configuração de estacionamento."""
        cursor = self.conn.cursor()
        query = """
            INSERT INTO parking_configurations (establishment_id, rows, columns, spot_type)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (establishment_id, rows, columns, spot_type))
        self.conn.commit()
        cursor.close()

    def get_parking_configurations(self, establishment_id):
        """Obtém as configurações de estacionamento de um estabelecimento."""
        cursor = self.conn.cursor()
        query = """
            SELECT id, rows, columns, spot_type, created_at
            FROM parking_configurations
            WHERE establishment_id = %s
        """
        cursor.execute(query, (establishment_id,))
        configurations = cursor.fetchall()
        cursor.close()

        return [
            {
                "id": row[0],
                "rows": row[1],
                "columns": row[2],
                "spot_type": row[3],
                "created_at": row[4],
            }
            for row in configurations
        ]

    def reserve_spot(self, parking_configuration_id, user_id, spot_number, reserved_until):
        """Reserva uma vaga para um usuário."""
        cursor = self.conn.cursor()
        query = """
            INSERT INTO occupied_spots (parking_configuration_id, user_id, spot_number, reserved_until)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (parking_configuration_id, user_id, spot_number, reserved_until))
        self.conn.commit()
        cursor.close()

    def get_occupied_spots(self, parking_configuration_id):
        """Obtém as vagas ocupadas de uma configuração de estacionamento."""
        cursor = self.conn.cursor()
        query = """
            SELECT spot_number, user_id, reserved_until
            FROM occupied_spots
            WHERE parking_configuration_id = %s
        """
        cursor.execute(query, (parking_configuration_id,))
        spots = cursor.fetchall()
        cursor.close()

        return [
            {"spot_number": row[0], "user_id": row[1], "reserved_until": row[2]}
            for row in spots
        ]

    def release_spot(self, parking_configuration_id, spot_number):
        """Libera uma vaga ocupada."""
        cursor = self.conn.cursor()
        query = """
            DELETE FROM occupied_spots
            WHERE parking_configuration_id = %s AND spot_number = %s
        """
        cursor.execute(query, (parking_configuration_id, spot_number))
        self.conn.commit()
        cursor.close()