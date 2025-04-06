from typing import Any
import mysql.connector
from config import DB_CONFIG

class User:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor(dictionary=True)
        self._create_table()

    def _create_table(self) -> None:
        query = """
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            senha VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""

        self.cursor.execute(query)
        self.connection.commit()

    def create_user(self, name, email, password):
        if self.cursor is None: 
            raise Exception("Não é possível criar um usuário no momento")
        
        sql_insert = f"INSERT INTO users (nome, email, senha) VALUES (%s, %s, %s)"
        values = (name, email, password)

        self.cursor.execute(sql_insert, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def read_user(self, email, password=None) -> Any:
        if password is not None:
            query = "SELECT * FROM users WHERE email = %s AND senha = %s"
            query_values = (email, password)

            self.cursor.execute(query, query_values)

        else:
            query = "SELECT * FROM users WHERE email = %s"
            query_values = (email,)

            self.cursor.execute(query, query_values)

        return self.cursor.fetchone() if self.cursor.fetchone() else None

    def update_password(self, email, new_password) -> bool:
        if self.cursor is None:
            raise Exception("Erro no cursor")

        query = f"UPDATE users SET senha = %s WHERE email = %s"
        query_values = (new_password, email)

        try:
            self.cursor.execute(query, query_values)
            self.connection.commit()

            return True

        except Exception as e:
            print(f"Erro: {e}")
            return False