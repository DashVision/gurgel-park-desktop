from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)
from controllers.auth.auth_controller import AuthController
from PyQt5.QtCore import Qt

class RegisterWindow(QWidget):
    def __init__(self, screens_controller):
        print("Iniciando construtor do RegisterWindow...")  # Log para depuração
        super().__init__()
        print("Chamando super().__init__() no RegisterWindow...")  # Log para depuração
        self.screens_controller = screens_controller
        print("Inicializando UI do RegisterWindow...")  # Log para depuração
        self.init_ui()
        print("RegisterWindow inicializado com sucesso!")  # Log para depuração

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Registrar nova conta")
        return_to_login_btn = QPushButton("Voltar para Login")
        return_to_login_btn.clicked.connect(self.handle_return_to_login)

        layout.addWidget(title)
        layout.addWidget(return_to_login_btn)

        self.setLayout(layout)

    def handle_return_to_login(self):
        self.screens_controller.set_screen("login")

# Teste isolado do RegisterWindow
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)

    register_window = RegisterWindow(None)  # Nenhum controlador necessário para o teste
    register_window.show()
    sys.exit(app.exec_())