from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from core.controllers.auth.auth_controller import AuthController

class LoginWindow(QWidget):
    def __init__(self, screens_controller, auth_controller):
        super().__init__()
        print("Inicializando LoginWindow...")  # Log para depuração
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller
        self.setWindowTitle("Login")
        self.setFixedSize(360, 640)  # Dimensões fixas para simular um celular
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)  # Espaçamento entre os elementos

        # Estilo geral da janela
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial, sans-serif;
            }
        """)

        

        # Título
        title = QLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color:  rgb(90, 0, 255);
            margin-bottom: 10px;
        """)

        # Logo
        logo_label = QLabel(self)
        pixmap = QPixmap("core/assets/logo gurgel park LTDA.png")  # Atualize com o caminho correto
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Campos de entrada
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Insira seu email")
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
                border:  rgb(90, 0, 255);
                background-color:  white;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Insira sua senha")
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
                border:  rgb(90, 0, 255);
                background-color:  white;
            }
        """)

        # Botões
        self.login_btn = QPushButton("Entrar")
        self.login_btn.setMinimumHeight(45)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color:  rgb(90, 0, 255);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color:  rgb(90, 0, 255);
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)

        self.forgot_password_btn = QPushButton("Esqueci minha senha")
        self.forgot_password_btn.setMinimumHeight(35)
        self.forgot_password_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #d5d5d5;
            }
        """)
        self.forgot_password_btn.clicked.connect(self.handle_forgot_password)

        self.register_btn = QPushButton("Registrar nova conta")
        self.register_btn.setMinimumHeight(35)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #d5d5d5;
            }
        """)
        self.register_btn.clicked.connect(self.handle_register)

        # Adicionando widgets ao layout
        layout.addWidget(title)
        layout.addWidget(logo_label, alignment=Qt.AlignTop)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.forgot_password_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def center_window(self):
        """Centraliza a janela na tela."""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def handle_login(self) -> None:
        print("Tentando fazer login...")

        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if email == "" or password == "":
            QMessageBox.warning(self, "Erro!", "Preencha os campos pelo menos")
            return

        if self.auth_controller.handle_login(email, password):
            user_type = self.auth_controller.get_current_user_type()
            if user_type == "cliente":
                self.screens_controller.set_screen("home")
            elif user_type == "estabelecimento":
                self.screens_controller.set_screen("establishment_home")
            QMessageBox.information(self, "Login", "Login realizado com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", "Credenciais inválidas!")
            print("Credenciais inválidas!")

    def handle_forgot_password(self):
        print("Navegando para a tela de 'Esqueci minha senha'...")
        self.screens_controller.set_screen("forgot_password")

    def handle_register(self):
        print("Navegando para a tela de 'Registrar'...")
        self.screens_controller.set_screen("register")

    def clear_fields(self):
        self.email_input.clear()
        self.password_input.clear()
