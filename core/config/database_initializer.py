from mysql.connector import connect, Error
from core.config.database_config import get_connection

def initialize_database():
    try:
        # Conecta ao MySQL sem especificar o banco de dados
        conn = connect(
            host="localhost",
            user="root",
            password="",
        )
        cursor = conn.cursor()

        # Cria o banco de dados se não existir
        cursor.execute("CREATE DATABASE IF NOT EXISTS gurgelpark_db;")
        print("Banco de dados 'gurgelpark_db' verificado/criado com sucesso.")

        # Usa o banco de dados
        cursor.execute("USE gurgelpark_db;")

        # Cria a tabela de usuários
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("Tabela 'users' verificada/criada com sucesso.")

        # Cria a tabela de veículos
        cursor.execute("""
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
        """)
        print("Tabela 'vehicles' verificada/criada com sucesso.")

        # Cria a tabela de notificações
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            vehicle_id INT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        );
        """)
        print("Tabela 'notifications' verificada/criada com sucesso.")

        # Cria a tabela de associação de veículos e usuários
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_id INT NOT NULL,
            user_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        print("Tabela 'vehicle_users' verificada/criada com sucesso.")

        # Cria a tabela de estabelecimentos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS establishments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            cnpj VARCHAR(14) NOT NULL UNIQUE,
            address TEXT NOT NULL,
            user_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        print("Tabela 'establishments' verificada/criada com sucesso.")

        # Cria a tabela de configurações de estacionamento
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_configurations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            establishment_id INT NOT NULL,
            `rows` INT NOT NULL,
            `columns` INT NOT NULL,
            spot_type ENUM('Normal', 'Preferencial', 'Reservada') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (establishment_id) REFERENCES establishments(id) ON DELETE CASCADE
        );
        """)
        print("Tabela 'parking_configurations' verificada/criada com sucesso.")

        # Cria a tabela de vagas ocupadas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS occupied_spots (
            id INT AUTO_INCREMENT PRIMARY KEY,
            parking_configuration_id INT NOT NULL,
            user_id INT NOT NULL,
            spot_number INT NOT NULL,
            reserved_until TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parking_configuration_id) REFERENCES parking_configurations(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        print("Tabela 'occupied_spots' verificada/criada com sucesso.")

        # Fecha a conexão
        cursor.close()
        conn.close()
        print("Inicialização do banco de dados concluída com sucesso.")

    except Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

if __name__ == "__main__":
    initialize_database()