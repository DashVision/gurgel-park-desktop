from core.config.database_config import get_connection

def initialize_database():
    print("Inicializando banco de dados...")
    conn = get_connection()
    cursor = conn.cursor()

    # Cria tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            user_type ENUM('cliente', 'estabelecimento') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("Tabela 'users' verificada/criada com sucesso.")

    # Cria tabela de estabelecimentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS establishments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            cnpj VARCHAR(14) UNIQUE NOT NULL,
            address TEXT NOT NULL,
            user_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    print("Tabela 'establishments' verificada/criada com sucesso.")

    # Cria tabela de veículos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            placa VARCHAR(7) NOT NULL,
            marca VARCHAR(50) NOT NULL,
            modelo VARCHAR(50) NOT NULL,
            ano INT NOT NULL,
            cor VARCHAR(20) NOT NULL,
            user_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    print("Tabela 'vehicles' verificada/criada com sucesso.")

    # Cria tabela de configurações de estacionamento
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_configurations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            establishment_id INT NOT NULL,
            `rows` INT NOT NULL,
            `columns` INT NOT NULL,
            spot_type ENUM('comum', 'deficiente', 'idoso') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (establishment_id) REFERENCES establishments(id) ON DELETE CASCADE
        )
    """)
    print("Tabela 'parking_configurations' verificada/criada com sucesso.")

    # Cria tabela de vagas ocupadas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS occupied_spots (
            id INT AUTO_INCREMENT PRIMARY KEY,
            parking_configuration_id INT NOT NULL,
            spot_number INT NOT NULL,
            user_id INT NOT NULL,
            reserved_until DATETIME NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parking_configuration_id) REFERENCES parking_configurations(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    print("Tabela 'occupied_spots' verificada/criada com sucesso.")

    # Cria tabela de notificações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            vehicle_id INT NOT NULL,
            message TEXT NOT NULL,
            read_at DATETIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        )
    """)
    print("Tabela 'notifications' verificada/criada com sucesso.")

    # Cria a tabela de benefícios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS benefits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            discount_value DECIMAL(5,2) NOT NULL,
            min_hours INT NOT NULL,
            establishment_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (establishment_id) REFERENCES establishments(id) ON DELETE CASCADE
        )
    """)
    print("Tabela 'benefits' verificada/criada com sucesso.")

    # Fecha a conexão
    cursor.close()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    initialize_database()