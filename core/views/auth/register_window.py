from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QComboBox)
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

        # Estilo geral da janela
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial;
            }
        """)

        # Título
        title = QLabel("Registrar nova conta")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)

        # Campos de entrada para nome, email e senha
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome")
        self.name_input.setMinimumHeight(40)
        self.name_input.setStyleSheet("""
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

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
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

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet("""
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

        # ComboBox para selecionar o tipo de usuário
        self.user_type_combo = QComboBox()
        self.user_type_combo.addItems(["cliente", "estabelecimento"])
        self.user_type_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                background-color: #fff;
            }
            QComboBox:focus {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)

        # Botão para registrar nova conta
        self.register_new_user_btn = QPushButton("Registrar nova conta")
        self.register_new_user_btn.setMinimumHeight(45)
        self.register_new_user_btn.setStyleSheet("""
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
        self.register_new_user_btn.clicked.connect(self.handle_register_new_user)

        # Botão para voltar ao login
        self.return_to_login_btn = QPushButton("Voltar para Login")
        self.return_to_login_btn.setMinimumHeight(40)
        self.return_to_login_btn.setStyleSheet("""
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
        self.return_to_login_btn.clicked.connect(self.handle_return_to_login)

        # Adicionando widgets ao layout
        layout.addWidget(title)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Tipo de Usuário:", alignment=Qt.AlignCenter))
        layout.addWidget(self.user_type_combo)
        layout.addWidget(self.register_new_user_btn)
        layout.addWidget(self.return_to_login_btn)

        self.setLayout(layout)

    def handle_register_new_user(self) -> None:
        # Captura os valores dos campos de entrada
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        user_type = self.user_type_combo.currentText()

        # Valida os campos
        if not name or not email or not password:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            # Valida o email e tenta registrar o usuário
            validated_email = Email(email)
            self.auth_controller.handle_register(name, str(validated_email), password, user_type)
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
