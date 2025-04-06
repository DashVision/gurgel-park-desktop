import mysql.connector
from config import DB_CONFIG

class Vehicle:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor(dictionary=True)
        self._create_table()

    def _create_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS vehicles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            placa VARCHAR(7) NOT NULL UNIQUE,
            marca VARCHAR(100) NOT NULL,
            modelo VARCHAR(100) NOT NULL,
            ano INT NOT NULL,
            cor VARCHAR(50) NOT NULL,
            user_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """

        self.cursor.execute(query)
        self.connection.commit()

    def register_vehicle(self, placa, marca, modelo, ano, cor, user_id) -> bool:
        if self.cursor == None:
            raise Exception("Erro no cursor")
        
        query = """
        INSERT INTO vehicles (placa, marca, modelo, ano, cor, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        try:
            self.cursor.execute(query, (placa, marca, modelo, ano, cor, user_id))
            self.connection.commit()

            return True

        except mysql.connector.Error as err:
            print(f"Erro ao cadastrar ve�culo: {err}")
            return False

    def get_vehicle_by_placa(self, placa) -> any:
        if self.cursor == None:
            raise Exception("Erro no cursor")

        query = "SELECT * FROM vehicles WHERE placa = %s"

        self.cursor.execute(query, (placa,))
        return self.cursor.fetchone()