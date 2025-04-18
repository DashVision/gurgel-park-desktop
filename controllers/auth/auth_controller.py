from repositories.auth.user_repository import UserRepository
from models.auth.user import User
import bcrypt

class AuthController:
    def __init__(self) -> None:
        print("Inicializando AuthController...")  # Log para depuração
        try:
            self.repository = UserRepository()
            print("AuthController inicializado com sucesso!")  # Log para depuração
        except Exception as e:
            print(f"Erro ao inicializar AuthController: {e}")
            raise

    def handle_login(self, email: str, password: str) -> bool:
        try:
            user = self.repository.get_user_by_credentials(email, password)

            if user:
                self.show_main_app(user.id)                
                return True

            return False

        except Exception as e:
            print(f"Erro no handle_login: {e}")
            return False
        
    def handle_register(self, name: str, email: str, password: str) -> bool:
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Salt é gerado como bytes

            user = User(name=name, email=email, hashed_password=hashed_password.decode('utf-8'))  # Decodifica o hash para armazenar como string
            self.repository.create_user(user)

            return True

        except Exception as e:
            print(f"Erro no handle_register: {e}")
            return False
        
    def handle_reset_password(self, email: str) -> bool:
        try:
            user = self.repository.get_user_by_email(email)

            if user:
                return True
            
            else:
                return False

        except Exception as e:
            print(f"Erro no handle_reset_password: {e}")
            return False

    def show_main_app(self, user_id):
        pass