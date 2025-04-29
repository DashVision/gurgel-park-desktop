from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt

from core.controllers.auth.auth_controller import AuthController

class NewPasswordWindow(QWidget):
    def __init__(self, screens_controller, auth_controller):
        super().__init__()
        print("Inicializando NewPasswordWindow...")
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Estilo geral da janela
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial;
            }
        """)

        # Título
        title = QLabel("Criar nova senha")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)

        # Campo Nova Senha
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Insira sua nova senha:")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setMinimumHeight(40)
        self.new_password_input.setStyleSheet("""
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

        # Campo Confirmar Nova Senha
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirme sua nova senha:")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setMinimumHeight(40)
        self.confirm_password_input.setStyleSheet("""
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

        # Botão Criar Senha
        self.create_password_btn = QPushButton("Criar Senha")
        self.create_password_btn.setMinimumHeight(45)
        self.create_password_btn.setStyleSheet("""
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
        self.create_password_btn.clicked.connect(self.handle_create_new_password)

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
        layout.addWidget(QLabel("Nova Senha:", alignment=Qt.AlignCenter))
        layout.addWidget(self.new_password_input)
        layout.addWidget(QLabel("Confirme a Nova Senha:", alignment=Qt.AlignCenter))
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.create_password_btn)
        layout.addWidget(self.return_to_login)
        layout.addStretch()

        self.setLayout(layout)

    def handle_create_new_password(self):
        email = self.auth_controller.current_email
        if not email:
            QMessageBox.warning(self, "Erro!", "Nenhum email associado à redefinição de senha.")
            return

        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if new_password == "" or confirm_password == "":
            QMessageBox.warning(self, "Erro!", "Preencha os campos pelo menos")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Erro!", "As senhas não coincidem")
            return

        if self.auth_controller.update_password(email, new_password):
            QMessageBox.information(self, "Sucesso!", "Senha atualizada com sucesso!")
            self.screens_controller.set_screen("login")
        else:
            QMessageBox.warning(self, "Erro!", "Não foi possível criar a nova senha.")

    def handle_return_to_login(self):
        self.screens_controller.set_screen("login")

    def clear_fields(self):
        self.new_password_input.clear()
        self.confirm_password_input.clear()
