from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from controllers.auth.RecoveryController import RecoveryController

class SwitchPasswordView(QWidget):
    def __init__(self, controller, email):
        super().__init__()
        
        self.controller = controller
        self.email = email
        self.main_layout = QVBoxLayout()
        self.initScreen()

    def initScreen(self):
        self.setWindowTitle("Insira sua nova senha")
        self.setWindowIcon(QIcon(""))
        
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

        self.generic_text = QLabel("Escolha uma nova senha: ")
        self.generic_text.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.generic_text)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Insira sua nova senha: ")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        container_layout.addWidget(self.new_password_input)

        self.confirm_btn = QPushButton("Confirmar nova senha")
        container_layout.addWidget(self.confirm_btn)

        container.setLayout(container_layout)
        self.main_layout.addWidget(container)
        self.setLayout(self.main_layout)

        self.confirm_btn.clicked.connect(lambda: self.handle_switch_password(self.new_password_input.text()))

    def clearFields(self):
        self.new_password_input.clear()

    def disableFields(self):
        self.new_password_input.setEnabled(False)
        self.confirm_btn.setEnabled(False)
        self.confirm_btn.setText("Senha atualizada com sucesso!")

    def handle_switch_password(self, new_password):
        if not new_password:
            QMessageBox.warning(self, "Erro", "Por favor, insira uma nova senha")
            return
            
        recovery_controller = RecoveryController(self.email)
        update_password = recovery_controller.switchPassoword(self.email, new_password)

        if update_password:
            QMessageBox.information(self, "Sucesso", "Senha atualizada com sucesso!")
            self.disableFields()
            self.controller.switch_to_login()
            
        else:
            QMessageBox.warning(self, "Erro", "Falha ao atualizar a senha")