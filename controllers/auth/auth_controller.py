from repositories.auth.user_repository import UserRepository
from models.auth.user import User
import bcrypt
from services.email_service import EmailService

class AuthController:
    def __init__(self) -> None:
        print("Inicializando AuthController...")  # Log para depuração
        try:
            self.repository = UserRepository()
            self.recovery_codes = {}
            self.current_email = None
            print("AuthController inicializado com sucesso!")  # Log para depuração

        except Exception as e:
            print(f"Erro ao inicializar AuthController: {e}")
            raise

    def handle_login(self, email: str, password: str) -> bool:
        try:
            user = self.repository.get_user_by_credentials(email)

            if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
                self.show_main_app(user.id)
                return True

            print("Credenciais inválidas.")  # Log para depuração
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
                recovery_code = EmailService.send_recovery_code(user.email)
                if recovery_code:
                    self.recovery_codes[email] = recovery_code
                    print(f"Código de recuperação enviado para {user.email}: {recovery_code}")
                    return True
                else:
                    print("Erro ao enviar o código de recuperação.")
                    return False
            else:
                print("Email não encontrado no banco de dados.")
                return False

        except Exception as e:
            print(f"Erro no handle_reset_password: {e}")
            return False

    def handle_confirm_code(self, email: str, code: str) -> bool:
        try:
            print(f"Validando código para o email: {email}")
            print(f"Código esperado: {self.recovery_codes.get(email)}")
            print(f"Código recebido: {code}")

            if email in self.recovery_codes and self.recovery_codes[email] == code:
                print(f"Código confirmado para o email: {email}")
                del self.recovery_codes[email]
                return True
            else:
                print(f"Código inválido ou expirado para o email: {email}")
                return False
            
        except Exception as e:
            print(f"Erro no handle_confirm_code: {e}")
            return False
        
    def update_password(self, email: str, new_password: str) -> bool:
        try:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self.repository.update_user_password(email, hashed_password.decode('utf-8'))
            return True
        
        except Exception as e:
            print(f"Erro no update_password: {e}")
            return False

    def show_main_app(self, user_id):
        pass