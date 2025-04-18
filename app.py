import sys
from PyQt5.QtWidgets import QApplication
from controllers.screens_controller import ScreensController
from views.auth.login_window import LoginWindow
from views.auth.forgot_password_window import ForgotPasswordWindow
from views.auth.register_window import RegisterWindow

def main():
    print("Inicializando o aplicativo...")  # Log para depuração
    app = QApplication(sys.argv)

    # Instancia o controlador de telas
    print("Instanciando o ScreensController...")  # Log para depuração
    screens_controller = ScreensController()

    # Cria as telas e adiciona ao controlador
    print("Criando as telas...")  # Log para depuração
    login_window = LoginWindow(screens_controller)
    forgot_password_window = ForgotPasswordWindow(screens_controller)
    register_window = RegisterWindow(screens_controller)

    screens_controller.add_screen("login", login_window)
    print("Tela de login adicionada ao ScreensController.")  # Log para depuração
    screens_controller.add_screen("forgot_password", forgot_password_window)
    print("Tela de recuperação de senha adicionada ao ScreensController.")  # Log para depuração
    screens_controller.add_screen("register", register_window)
    

    # Define a tela inicial como a tela de login
    print("Definindo a tela inicial como 'login'...")  # Log para depuração
    screens_controller.set_screen("login")

    # Exibe o controlador de telas
    print("Exibindo o ScreensController...")  # Log para depuração
    screens_controller.show()

    # Executa o loop principal do aplicativo
    print("Executando o loop principal do aplicativo...")  # Log para depuração
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()