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

        title = QLabel("Código de confirmação")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        instructions = QLabel("Digite o código enviado para seu email")
        instructions.setWordWrap(True)
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Insira o código:")
        self.code_input.setMinimumHeight(35)

        self.confirm_code_btn = QPushButton("Confirmar Código")
        self.confirm_code_btn.setMinimumHeight(40)
        self.confirm_code_btn.clicked.connect(self.handle_confirm_code)

        self.return_to_login = QPushButton("Voltar para Login")
        self.return_to_login.clicked.connect(self.handle_return_to_login)

        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(instructions)
        layout.addWidget(QLabel("Código:"))
        layout.addWidget(self.code_input)
        layout.addWidget(self.confirm_code_btn)
        layout.addWidget(self.return_to_login)
        
        layout.addStretch()

        self.setLayout(layout)

    def handle_confirm_code(self):
        code = self.code_input.text()
        email = self.auth_controller.current_email  # Recupera o email armazenado no AuthController

        print(f"Email recuperado do AuthController: {email}")  # Log para depuração

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