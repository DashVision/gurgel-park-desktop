from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from controllers.auth.RecoveryController import RecoveryController
from controllers.auth.LoginController import LoginController

class RecoveryView(QWidget):
    def __init__(self, controller):
        super().__init__()
        
        self.controller = controller
        self.main_layout = QVBoxLayout()
        self.second_layout = QVBoxLayout()
        
        self.initScreen()

    def initScreen(self):
        self.setWindowTitle("Recupere sua senha")
        self.setFixedSize(500, 500)
        self.setWindowIcon(QIcon('views/assets/carro-sedan-na-frente.png'))
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: 'Arial', sans-serif;
            }
            QLabel {
                font-size: 24px;
                color: #333;
                margin: 20px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                margin: 10px;
                background-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                margin: 10px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton#goback {
                background-color: #f44336;
            }
            QPushButton#goback:hover {
                background-color: #da190b;
            }
        """)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)

        logo_label = QLabel()
        logo_pixmap = QPixmap('views/assets/carro-sedan-na-frente.png')
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        logo_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(logo_label)

        self.recovery_generic_text = QLabel("Vamos te ajudar a recuperar sua senha!")
        self.recovery_generic_text.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.recovery_generic_text)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Insira seu email")
        container_layout.addWidget(self.email_input)

        self.confirm_btn = QPushButton("Enviar código de recuperação")
        container_layout.addWidget(self.confirm_btn)

        self.goback_btn = QPushButton("Retornar para a tela de login")
        self.goback_btn.setObjectName("goback")
        container_layout.addWidget(self.goback_btn)

        container.setLayout(container_layout)
        self.main_layout.addWidget(container)
        self.setLayout(self.main_layout)

        self.confirm_btn.clicked.connect(self.handle_recovery)
        self.goback_btn.clicked.connect(self.handle_goback)

    def codeConfirmScreen(self, code, email):
        self.setWindowTitle("Confirme o código recebido")
        self.setFixedSize(500, 500)
        self.setWindowIcon(QIcon('views/assets/carro-sedan-na-frente.png'))

        if self.layout():
            QWidget().setLayout(self.layout())

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)

        logo_label = QLabel()
        logo_pixmap = QPixmap('views/assets/carro-sedan-na-frente.png')
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(logo_label)

        self.confirm_generic_text = QLabel("Confirme o código recebido")
        self.confirm_generic_text.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.confirm_generic_text)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Insira o código recebido")
        container_layout.addWidget(self.code_input)

        self.confirm_btn = QPushButton("Confirmar código")
        container_layout.addWidget(self.confirm_btn)

        self.goback_btn = QPushButton("Voltar")
        self.goback_btn.setObjectName("goback")
        container_layout.addWidget(self.goback_btn)
        
        container.setLayout(container_layout)
        self.second_layout.addWidget(container)
        self.setLayout(self.second_layout)

        self.confirm_btn.clicked.connect(lambda: self.handle_code(code, email))
        self.goback_btn.clicked.connect(self.handle_goback)

    def codeSendRequest(self, email):
        verify_user = LoginController.verifyUserLogin(email)

        if verify_user is not None:
            controller = RecoveryController(email)
        
            if controller.code:
                self.codeConfirmScreen(controller.code, email)
            else:
                QMessageBox.warning(self, "Erro", "Falha ao enviar o código")

        else:
            QMessageBox.warning(self, "Erro", "O usuário não está cadastrado")

    def handle_code(self, code, email):
        code_input = self.code_input.text()

        if not code_input:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos")
            return
        
        if code_input != code:
            QMessageBox.warning(self, "Erro", "O código informado é diferente do código enviado!")
            return
        
        QMessageBox.information(self, "Sucesso", "Código confirmado com sucesso!")
        self.controller.switch_to_swpassword(email)

    def handle_recovery(self):
        email = self.email_input.text()

        if not email:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos")
            return
        
        self.codeSendRequest(email)

    def clearFields(self):
        try:
            if hasattr(self, 'email_input') and self.email_input is not None:
                self.email_input.clear()
                
            if hasattr(self, 'code_input') and self.code_input is not None:
                self.code_input.clear()
                
            if self.layout():
                QWidget().setLayout(self.layout())
                
            self.initScreen()
        except RuntimeError:
            pass

    def handle_goback(self):
        self.clearFields()
        self.controller.switch_to_login()