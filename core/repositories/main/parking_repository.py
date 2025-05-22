from core.config.database_config import get_connection

class ParkingRepository:
    def __init__(self):
        self.conn = get_connection()

    def create_parking_configuration(self, establishment_id, rows, columns, spot_type):
        """Cria uma configuração de estacionamento."""
        cursor = self.conn.cursor()
        query = """
            INSERT INTO parking_configurations (establishment_id, `rows`, `columns`, spot_type)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (establishment_id, rows, columns, spot_type))
        self.conn.commit()
        cursor.close()

    def get_parking_configurations(self, establishment_id):
        """Obtém as configurações de estacionamento de um estabelecimento."""
        cursor = self.conn.cursor()
        query = """
            SELECT id, `rows`, `columns`, spot_type, created_at
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
        """Reserva uma vaga para um usuário, impedindo concorrência."""
        cursor = self.conn.cursor()
        # Verifica se a vaga já está ocupada
        query_check = """
            SELECT COUNT(*) FROM occupied_spots
            WHERE parking_configuration_id = %s AND spot_number = %s AND reserved_until > NOW()
        """
        cursor.execute(query_check, (parking_configuration_id, spot_number))
        (count,) = cursor.fetchone()
        if count > 0:
            cursor.close()
            raise Exception("Esta vaga já está ocupada no período selecionado.")
        # Reserva a vaga
        query_insert = """
            INSERT INTO occupied_spots (parking_configuration_id, user_id, spot_number, reserved_until)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_insert, (parking_configuration_id, user_id, spot_number, reserved_until))
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

    def cancel_reservation(self, parking_configuration_id, spot_number, user_id):
        """Cancela a reserva de uma vaga feita por um usuário específico."""
        cursor = self.conn.cursor()
        query = """
            DELETE FROM occupied_spots
            WHERE parking_configuration_id = %s AND spot_number = %s AND user_id = %s
        """
        cursor.execute(query, (parking_configuration_id, spot_number, user_id))
        self.conn.commit()
        cursor.close()

    def release_spot(self, parking_configuration_id, spot_number):
        """Libera uma vaga ocupada (usado pelo estabelecimento)."""
        cursor = self.conn.cursor()
        query = """
            DELETE FROM occupied_spots
            WHERE parking_configuration_id = %s AND spot_number = %s
        """
        cursor.execute(query, (parking_configuration_id, spot_number))
        self.conn.commit()
        cursor.close()

    def get_reservations_expiring_until(self, until_datetime):
        """Busca reservas que vão expirar até determinado horário."""
        cursor = self.conn.cursor()
        query = """
            SELECT parking_configuration_id, spot_number, user_id, reserved_until
            FROM occupied_spots
            WHERE reserved_until > NOW() AND reserved_until <= %s
        """
        cursor.execute(query, (until_datetime.strftime("%Y-%m-%d %H:%M:%S"),))
        results = cursor.fetchall()
        cursor.close()
        return [
            {
                "parking_configuration_id": row[0],
                "spot_number": row[1],
                "user_id": row[2],
                "reserved_until": row[3].strftime("%Y-%m-%d %H:%M:%S") if hasattr(row[3], 'strftime') else str(row[3]),
            }
            for row in results
        ]