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

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)

        self.generic_text = QLabel("Escolha uma nova senha: ")
        self.generic_text.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.generic_text)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Insira sua nova senha: ")
        container_layout.addWidget(self.new_password_input)

        self.confirm_btn = QPushButton("Confirmar nova senha")
        container_layout.addWidget(self.confirm_btn)

        container.setLayout(container_layout)
        self.main_layout.addWidget(container)
        self.setLayout(self.main_layout)

        self.confirm_btn.clicked.connect(lambda: self.handle_switch_password(self.new_password_input.text()))

    def handle_switch_password(self, new_password):
        if not new_password:
            QMessageBox.warning(self, "Erro", "Por favor, insira uma nova senha")
            return
            
        recovery_controller = RecoveryController(self.email)
        update_password = recovery_controller.switchPassoword(self.email, new_password)

        if update_password:
            QMessageBox.information(self, "Sucesso", "Senha atualizada com sucesso!")
            self.controller.switch_to_login()
        else:
            QMessageBox.warning(self, "Erro", "Falha ao atualizar a senha")