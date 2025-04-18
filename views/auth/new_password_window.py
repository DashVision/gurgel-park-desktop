from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt

from controllers.auth.auth_controller import AuthController

class NewPasswordWindow(QWidget):
    def __init__(self, screens_controller, auth_controller):
        super().__init__()
        print("Inicializando NewPasswordWindow...")
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller  # Adiciona o auth_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Criar nova senha")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Insira sua nova senha:")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setMinimumHeight(35)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirme sua nova senha:")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setMinimumHeight(35)

        self.create_password_btn = QPushButton("Criar Senha")
        self.create_password_btn.setMinimumHeight(40)
        self.create_password_btn.clicked.connect(self.handle_create_new_password)

        self.return_to_login = QPushButton("Voltar para Login")
        self.return_to_login.clicked.connect(self.handle_return_to_login)

        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("Nova Senha:"))
        layout.addWidget(self.new_password_input)
        layout.addWidget(QLabel("Confirme a Nova Senha:"))
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.create_password_btn)
        layout.addWidget(self.return_to_login)

        layout.addStretch()
        self.setLayout(layout)

    def handle_create_new_password(self):
        # Recupera o email do AuthController
        email = self.auth_controller.current_email
        if not email:
            QMessageBox.warning(self, "Erro!", "Nenhum email associado à redefinição de senha.")
            return

        # Obtém as senhas inseridas pelo usuário
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Valida os campos
        if new_password == "" or confirm_password == "":
            QMessageBox.warning(self, "Erro!", "Preencha os campos pelo menos")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Erro!", "As senhas não coincidem")
            return

        # Atualiza a senha no AuthController
        if self.auth_controller.update_password(email, new_password):
            QMessageBox.information(self, "Sucesso!", "Senha atualizada com sucesso!")
            self.screens_controller.set_screen("login")
        else:
            QMessageBox.warning(self, "Erro!", "Não foi possível criar a nova senha.")

    def handle_return_to_login(self):
        self.screens_controller.set_screen("login")
