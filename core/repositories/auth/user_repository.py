from core.config.database_config import get_connection
from core.models.auth.user import User
from mysql.connector.errors import IntegrityError

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
        
        query = "INSERT INTO users (name, email, password, user_type) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (user.name, user.email, user.hashed_password, user.user_type))
            self.conn.commit()
            print("Usuário criado com sucesso!")  # Log para depuração

        except IntegrityError as e:
            if e.errno == 1062:  # Código de erro para duplicidade
                raise ValueError("Esse email já está cadastrado.")
            else:
                raise

        finally:
            cursor.close()

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
        print(f"Buscando usuário com email: {email}")  # Log para depuração
        cursor = self.conn.cursor()
        query = "SELECT id, name, email, password, user_type FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            print(f"Usuário encontrado: {row}")  # Log para depuração
            user = User(
                id=row[0],
                name=row[1],
                email=row[2],
                hashed_password=row[3],  # Certifique-se de que o hash está correto
                user_type=row[4]
            )
            return user

        print("Nenhum usuário encontrado.")  # Log para depuração
        return None

    def update_user_password(self, email: str, hashed_password: str) -> None:
        print(f"Atualizando senha para o email: {email}")  # Log para depuração
        cursor = self.conn.cursor()

        query = "UPDATE users SET password = %s WHERE email = %s"
        cursor.execute(query, (hashed_password, email))
        self.conn.commit()
        cursor.close()

        print("Senha atualizada com sucesso!")  # Log para depuração

    def update_user_password_with_id(self, user_id: int, hashed_password: str) -> None:
        print(f"Atualizando senha para o ID: {user_id}")  # Log para depuração
        cursor = self.conn.cursor()

        query = "UPDATE users SET password = %s WHERE id = %s"
        cursor.execute(query, (hashed_password, user_id))
        self.conn.commit()
        cursor.close()

        print("Senha atualizada com sucesso!")  # Log para depuração

    def update_user_email(self, user_id: int, new_email: str) -> None:
        print(f"Atualizando email para o ID: {user_id}")
        cursor = self.conn.cursor()

        query = "UPDATE users SET email = %s WHERE id = %s"
        cursor.execute(query, (new_email, user_id))
        self.conn.commit()
        cursor.close()

        print("Email atualizado com sucesso!") # Log para depuração

    def get_user_by_id(self, user_id):
        """Obtém um usuário pelo ID."""
        try:
            cursor = self.conn.cursor()
            query = "SELECT id, name, email FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            cursor.close()

            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                }
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário por ID: {e}")
            raise

    def delete_user(self, user_id: int) -> None:
        """Exclui um usuário pelo ID."""
        print(f"Deletando usuário com ID: {user_id}")  # Log para depuração
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            self.conn.commit()
            print("Usuário deletado com sucesso!")  # Log para depuração
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            raise
        finally:
            cursor.close()
