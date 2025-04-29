-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS gurgelpark_db;
USE gurgelpark_db;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    user_type ENUM('cliente', 'estabelecimento') DEFAULT 'cliente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de veículos
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

-- Tabela de notificações
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);

-- Tabela de associação de veículos e usuários
CREATE TABLE IF NOT EXISTS vehicle_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de estabelecimentos
CREATE TABLE IF NOT EXISTS establishments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    address TEXT NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de configurações de estacionamento
CREATE TABLE IF NOT EXISTS parking_configurations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    establishment_id INT NOT NULL,
    `rows` INT NOT NULL,
    `columns` INT NOT NULL,
    spot_type ENUM('Normal', 'Preferencial', 'Reservada') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (establishment_id) REFERENCES establishments(id) ON DELETE CASCADE
);

-- Tabela de vagas ocupadas
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