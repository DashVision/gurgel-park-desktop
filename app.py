import sys
from PyQt5.QtWidgets import QApplication
from application_initializer import initialize_application

def main():
    app = QApplication(sys.argv)

    # Inicializa o aplicativo
    screens_controller = initialize_application()

    # Define a tela inicial
    screens_controller.set_screen("login")

    # Exibe o controlador de telas
    screens_controller.show()

    # Executa o loop principal do aplicativo
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()