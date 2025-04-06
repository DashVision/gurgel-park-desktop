from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from views.auth.login_screen import LoginScreen
from views.auth.register_screen import RegisterScreen
from views.auth.forgot_password_screen import ForgotPasswordScreen
from views.auth.confirm_code_screen import ConfirmCodeScreen
from views.auth.reset_password_screen import ResetPasswordScreen

from controllers.auth.login_controller import LoginController
from controllers.auth.register_controller import RegisterController
from controllers.auth.recovery_controller import RecoveryController

class ScreensController:
    def __init__(self):
        self.login_controller = LoginController()
        self.register_controller = RegisterController()
        self.recovery_controller = RecoveryController()

        self.sm = ScreenManager()
        self._load_screens()

    def _load_screens(self):
        # Carrega os arquivos kv
        Builder.load_file('views/auth/kivys/login_screen.kv')
        Builder.load_file('views/auth/kivys/register_screen.kv')
        Builder.load_file('views/auth/kivys/forgot_password_screen.kv')
        Builder.load_file('views/auth/kivys/confirm_code_screen.kv')
        Builder.load_file('views/auth/kivys/reset_password_screen.kv')

        # Instancia as telas e adiciona ao ScreenManager
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(ForgotPasswordScreen(name='forgot'))
        self.sm.add_widget(ConfirmCodeScreen(name='confirm_code'))
        self.sm.add_widget(ResetPasswordScreen(name='reset_password'))

        self.sm.current = 'login'

    def get_root_widget(self):
        return self.sm


    # Métodos para manipulação de usuários e navegação entre telas
    def login_user(self, email, password):
        if self.login_controller.handle_user_login(email, password):
            print("Login realizado com sucesso!")
        else:
            print("Credenciais inválidas.")

    def register_user(self, name, email, password):
        if self.register_controller.create_user(name, email, password):
            print("Usuário registrado com sucesso!")
            self.show_login_screen()
        else:
            print("Erro no cadastro. Verifique se o email já está em uso.")

    def reset_password(self, email, new_password):
        if self.recovery_controller.switch_password(email, new_password):
            print("Senha redefinida com sucesso!")
            self.show_login_screen()
        else:
            print("Erro ao redefinir a senha. Verifique o email informado.")

    def send_recovery_code(self, email):
        if self.recovery_controller.send_recovery_code(email):
            print("Código enviado com sucesso")
            self.show_confirm_code_screen()
        else:
            print("Erro ao enviar código")

    def confirm_code(self, user_input_code, code):
        if user_input_code == code:
            print("Código confirmado com sucesso, escolha sua nova senha")
            self.show_reset_password_screen()
        else:
            print("Código incorreto")

    def show_login_screen(self):
        self.sm.current = 'login'

    def show_register_screen(self):
        self.sm.current = 'register'

    def show_forgot_password_screen(self):
        self.sm.current = 'forgot'

    def show_confirm_code_screen(self):
        self.sm.current = 'confirm_code'

    def show_reset_password_screen(self):
        self.sm.current = 'reset_password'