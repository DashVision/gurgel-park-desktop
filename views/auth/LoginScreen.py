from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from controllers.auth.LoginController import LoginController

class LoginViews(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.main_layout = QHBoxLayout() 
        self.form_layout = QVBoxLayout()

        self.initScreen()

    def initScreen(self):
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon(" "))  

        self.setFixedSize(1000, 500) 
        self.setWindowIcon(QIcon('views/assets/carro-sedan-na-frente.png'))

        self.img_label = QLabel(self)
        pixmap = QPixmap('')  # views/assets/depositphotos_23701387-stock-photo-man-with-car-keys.jpg
        self.img_label.setPixmap(pixmap)
        self.img_label.setAlignment(Qt.AlignLeft)
        self.img_label.setScaledContents(True)  
        self.img_label.setFixedSize(400, 500)  

        self.welcome_generic_text = QLabel("Seja bem-vindo ao Gurgel Park")
        self.welcome_generic_text.setAlignment(Qt.AlignCenter)
        self.welcome_generic_text.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; margin-bottom: 20px;")
        self.form_layout.addWidget(self.welcome_generic_text)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Insira seu email")
        self.form_layout.addWidget(self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Insira sua senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addWidget(self.password_input)

        self.confirm_btn = QPushButton("Confirmar")
        self.confirm_btn.setObjectName("confirm_btn")
        self.confirm_btn.clicked.connect(self.handle_login)
        self.form_layout.addWidget(self.confirm_btn)
        
        self.goto_register_btn = QPushButton("Ainda não possui login? Realize o cadastro!")
        self.goto_register_btn.clicked.connect(self.handle_goto_register)
        self.form_layout.addWidget(self.goto_register_btn)

        self.recovery_password_btn = QPushButton("Esqueceu sua senha?")
        self.recovery_password_btn.clicked.connect(self.handle_goto_recovery)
        self.form_layout.addWidget(self.recovery_password_btn)

        self.main_layout.addWidget(self.img_label) 
        self.main_layout.addLayout(self.form_layout)  

        self.setLayout(self.main_layout)

        self.setStyleSheet("""
            QWidget {
                background: transparent;
                color: #333;
                font-family: 'Arial', sans-serif;
            }
            
            QLabel {
                border-right: 2px solid #ddd;
            }

            QLabel#welcome_generic_text {
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
                margin-bottom: 20px;
            }

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

            QPushButton#confirm_btn {
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

            QPushButton#confirm_btn:hover {
                background-color: #45a049;
            }

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

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not all([email, password]):
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos!")
            return

        login_auth = LoginController.verifyUserLogin(email, password)
        
        if login_auth:
            QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")
            self.controller.switch_to_home(email)
            return
        
        QMessageBox.warning(self, "Erro", "Email ou senha incorretos!")

    def handle_goto_register(self):
        self.clearFields()
        self.controller.switch_to_register()

    def handle_goto_recovery(self):
        self.clearFields()
        self.controller.switch_to_recovery()

    def clearFields(self):
        self.email_input.clear()
        self.password_input.clear()