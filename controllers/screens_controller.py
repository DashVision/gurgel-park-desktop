# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import ScreenManager, Screen
from controllers.auth.login_controller import LoginController
from controllers.auth.register_controller import RegisterController
from controllers.auth.recovery_controller import RecoveryController

class ScreensController:
    def __init__(self) -> None:
        self.login_controller = LoginController
        self.register_controller = RegisterController
        self.recovery_controller = RecoveryController

        self.sm = ScreenManager()
        self._load_screens()

    def _load_screens(self) -> None:
        from kivy.lang import Builder
        
        login_screen = Builder.load_file('views/auth/login.kv')
        register_screen = Builder.load_file('views/auth/register.kv')
        forgot_screen = Builder.load_file('views/auth/forgot_password.kv')
        confirm_code_screen = Builder.load_file('views/auth/confirm_code.kv')
        reset_password_screen = Builder.load_file('views/auth/reset_password.kv')

        screen_login = Screen(name='login')
        screen_login.add_widget(login_screen)
        self.sm.add_widget(screen_login)

        screen_register = Screen(name='register')
        screen_register.add_widget(register_screen)
        self.sm.add_widget(screen_register)

        screen_forgot = Screen(name='forgot')
        screen_forgot.add_widget(forgot_screen)
        self.sm.add_widget(screen_forgot)

        screen_confirm_code = Screen(name='confirm_code')
        screen_confirm_code.add_widget(confirm_code_screen)
        self.sm.add_widget(screen_confirm_code)

        screen_reset_password = Screen(name='reset_password')
        screen_reset_password.add_widget(reset_password_screen)
        self.sm.add_widget(screen_reset_password)

        self.sm.current = 'login'

    def get_root_widget(self) -> ScreenManager:
        return self.sm

    def login_user(self, email, password): # Realizar implementação real
        if self.login_controller.handle_user_login(email, password):
            print("Login realizado com sucesso!")
           
        else:
            print("Credenciais inválidas.") 

    def register_user(self, name, email, password): # Realizar implementação real
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