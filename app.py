import sys
from PyQt5.QtWidgets import QApplication
from controllers.screens_controller import ScreensController
from controllers.auth.auth_controller import AuthController
from views.auth.login_window import LoginWindow
from views.auth.forgot_password_window import ForgotPasswordWindow
from views.auth.register_window import RegisterWindow
from views.auth.new_password_window import NewPasswordWindow
from views.auth.confirm_code_window import ConfirmCodeWindow
from views.home.home_window import HomeWindow

def main():
    print("Inicializando o aplicativo...")  # Log para depuração
    app = QApplication(sys.argv)

    # Instancia o controlador de telas
    print("Instanciando o ScreensController...")  # Log para depuração
    screens_controller = ScreensController()

    # Instancia o AuthController compartilhado
    auth_controller = AuthController()

    # Cria as telas e adiciona ao controlador
    print("Criando as telas...")  # Log para depuração
    login_window = LoginWindow(screens_controller, auth_controller)
    forgot_password_window = ForgotPasswordWindow(screens_controller, auth_controller)
    register_window = RegisterWindow(screens_controller, auth_controller)
    new_password_window = NewPasswordWindow(screens_controller, auth_controller)
    confirm_code_window = ConfirmCodeWindow(screens_controller, auth_controller)

    # Telas pós login
    home_window = HomeWindow(screens_controller, auth_controller)

    screens_controller.add_screen("login", login_window)
    screens_controller.add_screen("forgot_password", forgot_password_window)
    screens_controller.add_screen("register", register_window)
    screens_controller.add_screen("new_password", new_password_window)
    screens_controller.add_screen("confirm_code", confirm_code_window)
    screens_controller.add_screen("home", home_window)

    screens_controller.auth_controller = auth_controller

    screens_controller.set_screen("login")

    # Exibe o controlador de telas
    print("Exibindo o ScreensController...")  # Log para depuração
    screens_controller.show()

    # Executa o loop principal do aplicativo
    print("Executando o loop principal do aplicativo...")  # Log para depuração
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()