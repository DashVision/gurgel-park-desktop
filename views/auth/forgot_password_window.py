from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)
from controllers.auth.auth_controller import AuthController
from PyQt5.QtCore import Qt

class ForgotPasswordWindow(QWidget):
    def __init__(self, screens_controller):
        super().__init__()
        print("Inicializando ForgotPasswordWindow...")  # Log para depuração
        self.auth_controller = AuthController()
        self.screens_controller = screens_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Esqueci minha senha")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        instructions = QLabel("Digite seu email para receber instruções de recuperação de senha")
        instructions.setWordWrap(True)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Insira seu email:")
        self.email_input.setMinimumHeight(35)

        self.reset_password_btn = QPushButton("Redefinir Senha")
        self.reset_password_btn.setMinimumHeight(40)
        self.reset_password_btn.clicked.connect(self.handle_reset_password)

        self.return_to_login = QPushButton("Voltar para Login")
        self.return_to_login.clicked.connect(self.handle_return_to_login)

        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(instructions)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(self.reset_password_btn)
        layout.addWidget(self.return_to_login)
        
        layout.addStretch()

        self.setLayout(layout)

    def handle_reset_password(self):
        email = self.email_input.text()

        if not email:
            QMessageBox.warning(self, "Erro", "Por favor, preencha o campo de email.")
            return

        if self.auth_controller.handle_reset_password(email):
            QMessageBox.information(self, "Sucesso", "Instruções para redefinir a senha foram enviadas para seu email.")
            self.screens_controller.set_screen("login")
            
        else:
            QMessageBox.warning(self, "Erro", "Email não encontrado.")

    def handle_return_to_login(self):
        self.screens_controller.set_screen("login")