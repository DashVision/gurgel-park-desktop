from core.repositories.auth.user_repository import UserRepository
from core.models.auth.user import User
from core.services.email_service import EmailService
import bcrypt
from typing import Optional

class AuthController:
    def __init__(self) -> None:
        print("Inicializando AuthController...")  # Log para depuração
        try:
            self.repository = UserRepository()
            self.recovery_codes = {}
            self.current_email = None
            self.current_user = None  # Armazena o usuário logado
            print("AuthController inicializado com sucesso!")  # Log para depuração

        except Exception as e:
            print(f"Erro ao inicializar AuthController: {e}")
            raise

    def is_logged_in(self) -> bool:
        is_logged = self.current_email is not None
        print(f"is_logged_in: {is_logged}")
        return is_logged
    
    def logout(self) -> None:
        self.current_email = None
        print("Usuário deslogado.")

    def handle_login(self, email: str, password: str) -> bool:
        try:
            user = self.repository.get_user_by_email(email)
            if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
                self.current_email = user.email
                self.current_user = user  # Certifique-se de que o campo `id` está preenchido
                print(f"Usuário logado: {self.current_user}")  # Log para depuração
                return True
            print("Credenciais inválidas.")  # Log para depuração
            return False
        except Exception as e:
            print(f"Erro no handle_login: {e}")
            return False
        
    def handle_register(self, name: str, email: str, password: str) -> bool:
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user = User(name=name, email=email, hashed_password=hashed_password)
            self.repository.create_user(user)

            return True

        except ValueError as e:
            print(f"Erro no handle_register: {e}")
            raise  # Propaga a exceção para a interface

        except Exception as e:
            print(f"Erro inesperado no handle_register: {e}")
            raise  # Propaga exceções inesperadas
        
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
        
    def get_current_user_id(self) -> Optional[int]:
        if self.current_user:
            print(f"get_current_user_id: Usuário atual: {self.current_user}")
            return self.current_user.id
        print("get_current_user_id: Nenhum usuário está logado.")
        return None