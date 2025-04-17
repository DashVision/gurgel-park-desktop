from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from controllers.auth.auth_controller import AuthController
from models.auth.email import Email  # Importando a classe Email


class RegisterWindow(QWidget):
    def __init__(self, screens_controller, auth_controller=None):
        super().__init__()
        self.auth_controller = AuthController()
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
        title.setAlignment(Qt.AlignCenter)
        
        self.register_new_user_btn = QPushButton("Registrar nova conta")
        self.register_new_user_btn.clicked.connect(self.handle_register_new_user)

        self.return_to_login_btn = QPushButton("Voltar para Login")
        self.return_to_login_btn.clicked.connect(self.handle_return_to_login)

        layout.addWidget(title)
        layout.addWidget(self.return_to_login_btn)

        self.setLayout(layout)

    def handle_register_new_user(self, name: str, email: str, password: str) -> None:
        try:
            validated_email = Email(email)
            if self.auth_controller.handle_register(name, str(validated_email), password):
                QMessageBox.information(self, "Sucesso", "Usuário registrado com sucesso!")
                self.screens_controller.set_screen("login")

            else:
                QMessageBox.critical(self, "Erro", "Erro ao registrar o usuário.")
                
        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

    def handle_return_to_login(self) -> None:
        self.screens_controller.set_screen("login")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)

    register_window = RegisterWindow(None)  # Nenhum controlador necessário para o teste
    register_window.show()
    sys.exit(app.exec_())