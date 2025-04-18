from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt

from controllers.auth.auth_controller import AuthController

class LoginWindow(QWidget):
    def __init__(self, screens_controller, auth_controller):
        super().__init__()
        print("Inicializando LoginWindow...")  # Log para depuração
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller  # Adiciona o auth_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Login")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Insira seu email:")
        self.email_input.setMinimumHeight(35)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Insira sua senha:")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)

        self.login_btn = QPushButton("Entrar")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.clicked.connect(self.handle_login)

        self.forgot_password_btn = QPushButton("Esqueci minha senha")
        self.forgot_password_btn.clicked.connect(self.handle_forgot_password)

        self.register_btn = QPushButton("Registrar nova conta")
        self.register_btn.clicked.connect(self.handle_register)

        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Senha:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.forgot_password_btn)
        layout.addWidget(self.register_btn)
        
        layout.addStretch()
        
        self.setLayout(layout)

    def handle_login(self) -> None:
        print("Tentando fazer login...")

        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if email == "" or password == "":
            QMessageBox.warning(self, "Erro!", "Preencha os campos pelo menos")
            return

        if self.auth_controller.handle_login(email, password):
            QMessageBox.information(self, "Login", "Login realizado com sucesso!")
            self.screens_controller.set_screen("main_app")

        else:
            QMessageBox.warning(self, "Erro", "Credenciais inválidas!")
            print("Credenciais inválidas!")

    def handle_forgot_password(self):
        print("Navegando para a tela de 'Esqueci minha senha'...")  # Log para depuração
        self.screens_controller.set_screen("forgot_password")

    def handle_register(self):
        print("Navegando para a tela de 'Registrar'...")  # Log para depuração
        self.screens_controller.set_screen("register")