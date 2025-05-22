from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from core.controllers.auth.auth_controller import AuthController

class ConfirmCodeWindow(QWidget):
    def __init__(self, screens_controller, auth_controller):
        super().__init__()
        print("Inicializando ConfirmCodeWindow...")  # Log para depuração
        self.auth_controller = auth_controller  # Usa a instância compartilhada
        self.screens_controller = screens_controller
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
        title = QLabel("Código de confirmação")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)

        # Instruções
        instructions = QLabel("Digite o código enviado para seu email")
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("""
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
        """)

        # Campo de texto
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Insira o código:")
        self.code_input.setMinimumHeight(40)
        self.code_input.setStyleSheet("""
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

        # Botão Confirmar Código
        self.confirm_code_btn = QPushButton("Confirmar Código")
        self.confirm_code_btn.setMinimumHeight(45)
        self.confirm_code_btn.setStyleSheet("""
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
        self.confirm_code_btn.clicked.connect(self.handle_confirm_code)

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
        layout.addWidget(QLabel("Código:", alignment=Qt.AlignCenter))
        layout.addWidget(self.code_input)
        layout.addWidget(self.confirm_code_btn)
        layout.addWidget(self.return_to_login)
        layout.addStretch()

        self.setLayout(layout)

    def handle_confirm_code(self):
        code = self.code_input.text()
        email = self.auth_controller.current_email

        print(f"Email recuperado do AuthController: {email}")

        if not code:
            QMessageBox.warning(self, "Erro", "Por favor, preencha o campo de código.")
            return

        if self.auth_controller.handle_confirm_code(email, code):
            QMessageBox.information(self, "Sucesso", "Código confirmado com sucesso.")
            self.screens_controller.set_screen("new_password")
        else:
            QMessageBox.warning(self, "Erro", "Código inválido ou expirado.")

    def handle_return_to_login(self):
        self.screens_controller.set_screen("login")

    def clear_fields(self):
        self.code_input.clear()