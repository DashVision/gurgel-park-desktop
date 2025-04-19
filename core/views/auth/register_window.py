from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from core.controllers.auth.auth_controller import AuthController
from core.controllers.screens_controller import ScreensController
from core.models.auth.email import Email  # Importando a classe Email


class RegisterWindow(QWidget):
    def __init__(self, screens_controller, auth_controller=None):
        super().__init__()
        self.auth_controller = AuthController()
        self.screens_controller = screens_controller
        print("Iniciando construtor do RegisterWindow...")  # Log para depuração
        print("Inicializando UI do RegisterWindow...")  # Log para depuração
        self.init_ui()
        print("RegisterWindow inicializado com sucesso!")  # Log para depuração

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Registrar nova conta")
        title.setAlignment(Qt.AlignCenter)

        # Campos de entrada para nome, email e senha
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Botão para registrar nova conta
        self.register_new_user_btn = QPushButton("Registrar nova conta")
        self.register_new_user_btn.clicked.connect(self.handle_register_new_user)

        # Botão para voltar ao login
        self.return_to_login_btn = QPushButton("Voltar para Login")
        self.return_to_login_btn.clicked.connect(self.handle_return_to_login)

        # Adicionando widgets ao layout
        layout.addWidget(title)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_new_user_btn)
        layout.addWidget(self.return_to_login_btn)

        self.setLayout(layout)

    def handle_register_new_user(self) -> None:
        # Captura os valores dos campos de entrada
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        # Valida os campos
        if not name or not email or not password:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            # Valida o email e tenta registrar o usuário
            validated_email = Email(email)
            self.auth_controller.handle_register(name, str(validated_email), password)
            QMessageBox.information(self, "Sucesso", "Usuário registrado com sucesso!")
            self.screens_controller.set_screen("login")

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))  # Exibe a mensagem de erro específica

        except Exception as e:
            QMessageBox.critical(self, "Erro", "Erro inesperado ao registrar o usuário.")
            print(f"Erro inesperado: {e}")  # Log para depuração

    def handle_return_to_login(self) -> None:
        print("Tentando voltar para a tela de login...")  # Log para depuração
        self.screens_controller.set_screen("login")

    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.password_input.clear()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)

    register_window = RegisterWindow(None)  # Nenhum controlador necessário para o teste
    register_window.show()
    sys.exit(app.exec_())