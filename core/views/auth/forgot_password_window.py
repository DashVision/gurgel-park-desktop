from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)
from core.controllers.auth.auth_controller import AuthController
from PyQt5.QtCore import Qt

class ForgotPasswordWindow(QWidget):
    def __init__(self, screens_controller, auth_controller):
        super().__init__()
        print("Inicializando ForgotPasswordWindow...")  # Log para depuração
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Estilo da janela inteira
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial;
            }
        """)

        # Título
        title = QLabel("Esqueci minha senha")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)

        # Instruções
        instructions = QLabel("Digite seu email para receber instruções de recuperação de senha")
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("""
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
        """)

        # Campo de email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Insira seu email:")
        self.email_input.setMinimumHeight(40)
        self.email_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                background-color: #fff;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)

        # Botão Redefinir Senha
        self.reset_password_btn = QPushButton("Redefinir Senha")
        self.reset_password_btn.setMinimumHeight(45)
        self.reset_password_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.reset_password_btn.clicked.connect(self.handle_reset_password)

        # Botão Voltar para Login
        self.return_to_login = QPushButton("Voltar para Login")
        self.return_to_login.setMinimumHeight(40)
        self.return_to_login.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #d5d5d5;
            }
        """)
        self.return_to_login.clicked.connect(self.handle_return_to_login)

        # Layout
        layout.addWidget(title)
        layout.addWidget(instructions)
        layout.addWidget(QLabel("Email:", alignment=Qt.AlignCenter))
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
            self.auth_controller.current_email = email  # Armazena o email no AuthController
            print(f"Email armazenado no AuthController: {self.auth_controller.current_email}")

            QMessageBox.information(self, "Sucesso", "Instruções para redefinir a senha foram enviadas para seu email.")
            self.screens_controller.set_screen("confirm_code")
        else:
            QMessageBox.warning(self, "Erro", "Email não encontrado.")

    def handle_return_to_login(self):
        self.screens_controller.set_screen("login")

    def clear_fields(self):
        self.email_input.clear()
