from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from controllers.RegisterController import RegisterController

class RegisterViews(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.mainLayout = QHBoxLayout()
        self.formLayout = QVBoxLayout()

        self.initScreen()

    def initScreen(self):
        self.setWindowTitle("Registro")
        self.setWindowIcon(QIcon(""))
        self.setFixedSize(1000, 500)
        self.setWindowIcon(QIcon('icons\carro-sedan-na-frente.png'))

        self.img_label = QLabel(self)
        pixmap = QPixmap('icons\depositphotos_23701387-stock-photo-man-with-car-keys.jpg')
        self.img_label.setPixmap(pixmap)
        self.img_label.setAlignment(Qt.AlignLeft)
        self.img_label.setScaledContents(True)
        self.img_label.setFixedSize(400, 500)

        self.welcome_text = QLabel("Criar nova conta")
        self.welcome_text.setAlignment(Qt.AlignCenter)
        self.welcome_text.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; margin-bottom: 20px;")
        self.formLayout.addWidget(self.welcome_text)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome completo")
        self.formLayout.addWidget(self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.formLayout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.formLayout.addWidget(self.password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmar senha")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.formLayout.addWidget(self.confirm_password_input)

        self.register_btn = QPushButton("Registrar")
        self.register_btn.setObjectName("register_btn")
        self.register_btn.clicked.connect(self.handle_register)
        self.formLayout.addWidget(self.register_btn)

        self.goto_login_btn = QPushButton("Já possui uma conta? Faça login!")
        self.goto_login_btn.clicked.connect(self.handle_goto_login)
        self.formLayout.addWidget(self.goto_login_btn)

        self.mainLayout.addWidget(self.img_label)
        self.mainLayout.addLayout(self.formLayout)
        self.setLayout(self.mainLayout)

        self.setStyleSheet("""
            /* Estilo geral */
            QWidget {
                background: transparent;
                color: #333;
                font-family: 'Arial', sans-serif;
            }
            
            /* Imagem à esquerda */
            QLabel {
                border-right: 2px solid #ddd;
            }

            /* Texto de boas-vindas */
            QLabel#welcome_text {
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
                margin-bottom: 20px;
            }

            /* Campos de entrada */
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: #333;
                background-color: white;
                margin: 10px 0;
                max-width: 400px;
            }

            /* Botão principal */
            QPushButton#register_btn {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 20px;
                width: 200px;
                align-self: center;
            }

            QPushButton#register_btn:hover {
                background-color: #45a049;
            }

            /* Botões de texto */
            QPushButton {
                background: none;
                color: #4CAF50;
                border: none;
                font-size: 14px;
                padding: 10px;
                text-align: center;
            }

            QPushButton:hover {
                text-decoration: underline;
            }
        """)

    def handle_register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not all([name, email, password, confirm_password]):
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem!")
            return

        RegisterController.createUser(name, email, password)
        QMessageBox.information(self, "Sucesso", "Registro realizado com sucesso!")
        self.handle_goto_login()

    def handle_goto_login(self):
        self.controller.switch_to_login()
