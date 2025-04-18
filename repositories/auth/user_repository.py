from config.database_config import get_connection
from models.auth.user import User

from typing import Optional

class UserRepository:
    def __init__(self) -> None:
        print("Inicializando UserRepository...")  # Log para depuração
        try:
            self.conn = get_connection()
            print("Conexão com o banco de dados estabelecida!")  # Log para depuração
        except Exception as e:
            print(f"Erro ao inicializar UserRepository: {e}")
            raise

    def __del__(self) -> None:
        if self.conn.is_connected():
            print("Fechando conexão com o banco de dados...")  # Log para depuração
            self.conn.close()

    def create_user(self, user: User) -> None:
        print(f"Criando usuário: {user}")  # Log para depuração
        cursor = self.conn.cursor()
        
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (user.name, user.email, user.hashed_password))
        self.conn.commit()
        cursor.close()
        print("Usuário criado com sucesso!")  # Log para depuração

    def get_user_by_credentials(self, email: str) -> Optional[User]:
        print(f"Buscando usuário com email: {email}")  # Log para depuração
        cursor = self.conn.cursor()
        query = "SELECT id, name, email, password FROM users WHERE email = %s"
        cursor.execute(query, (email,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            print(f"Usuário encontrado: {row}")  # Log para depuração
            user = User(
                id=row[0],
                name=row[1],
                email=row[2],
                hashed_password=row[3]  # Retorna o hash armazenado
            )
            return user

        print("Nenhum usuário encontrado.")  # Log para depuração
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        print(f"Buscando usuário com email: {email}")
        cursor = self.conn.cursor()

        query = "SELECT id, name, email, password FROM users WHERE email = %s"
        cursor.execute(query, (email,))

        row = cursor.fetchone()
        cursor.close()

        if row:
            print(f"Usuário encontrado: {row}")
            user = User(
                id=row[0],
                name=row[1],
                email=row[2],
                hashed_password=row[3]
            )
            return user
        
        print("Nenhum usuário encontrado.")
        return None
    
    def update_password(self, user_id: int, new_password: str) -> None:
        print(f"Atualizando senha do usuário com ID: {user_id}")
        cursor = self.conn.cursor()

        query = "UPDATE users SET password = %s WHERE id = %s"
        cursor.execute(query, (new_password, user_id))

        self.conn.commit()
        cursor.close()
        
        print("Senha atualizada com sucesso!")