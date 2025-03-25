from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class LoginViews(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QHBoxLayout() 
        self.form_layout = QVBoxLayout()  

        self.initScreen()

    def initScreen(self):
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon(" "))  

        self.setFixedSize(1000, 500) 
        self.setWindowIcon(QIcon('icons\carro-sedan-na-frente.png'))

        self.img_label = QLabel(self)
        pixmap = QPixmap('icons\depositphotos_23701387-stock-photo-man-with-car-keys.jpg')  
        self.img_label.setPixmap(pixmap)
        self.img_label.setAlignment(Qt.AlignLeft)
        self.img_label.setScaledContents(True)  # Ajusta a imagem para o tamanho da label
        self.img_label.setFixedSize(400, 500)  # Tamanho máximo da label

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
        self.form_layout.addWidget(self.confirm_btn)
        
        self.goto_register_btn = QPushButton("Ainda não possui login? Realize o cadastro!")
        self.form_layout.addWidget(self.goto_register_btn)

        self.recovery_password_btn = QPushButton("Esqueceu sua senha?")
        self.form_layout.addWidget(self.recovery_password_btn)

        self.main_layout.addWidget(self.img_label) 
        self.main_layout.addLayout(self.form_layout)  

        self.setLayout(self.main_layout)

        self.setStyleSheet("""
            /* Estilo geral */
            QWidget {
                background-color: #f5f5f5;
                color: #333;
                font-family: 'Arial', sans-serif;
            }
            
            /* Imagem à esquerda */
            QLabel {
                border-right: 2px solid #ddd;
            }

            /* Texto de boas-vindas */
            QLabel#welcome_generic_text {
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
                background-color: #fff;
                margin: 10px 0;
                max-width: 400px;
            }

            QLineEdit:focus {
                border-color: #4CAF50;
            }

            /* Botão Confirmar */
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

            /* Botões de fundo invisível */
            QPushButton:!pressed {
                background: none;
                color: #4CAF50;
                border: none;
                font-size: 14px;
                padding: 10px;
                text-align: center;
                width: 200px;
                align-self: center;
            }

            QPushButton:!pressed:hover {
                text-decoration: underline;
            }

            /* Estilo para o texto de fundo invisível */
            QPushButton#goto_register_btn {
                font-size: 14px;
                margin-top: 10px;
                text-align: center;
            }

            QPushButton#recovery_password_btn {
                font-size: 14px;
                margin-top: 5px;
                text-align: center;
            }

            /* Formatação do layout */
            QVBoxLayout {
                padding: 20px;
                align-items: center;
            }

            /* Ajustando o layout da tela para centralizar os campos de login */
            QHBoxLayout {
                justify-content: center;
            }

            /* Adicionando espaçamento entre os botões */
            QPushButton {
                margin-top: 15px;
            }
        """)
