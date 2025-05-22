from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QMessageBox, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt

class EstablishmentRegisterWindow(QWidget):
    def __init__(self, screens_controller, establishments_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.establishments_controller = establishments_controller
        self.init_ui()

    def init_ui(self):
        # Estilo da janela inteira
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial;
            }
        """)

        layout = QVBoxLayout()

        # Título
        title = QLabel("Cadastro de Estabelecimento")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)

        # Formulário
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome do Estabelecimento")
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

        self.cnpj_input = QLineEdit()
        self.cnpj_input.setPlaceholderText("CNPJ (somente números)")
        self.cnpj_input.setMinimumHeight(40)
        self.cnpj_input.setStyleSheet("""
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

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Endereço")
        self.address_input.setMinimumHeight(40)
        self.address_input.setStyleSheet("""
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

        form_layout.addRow("Nome:", self.name_input)
        form_layout.addRow("CNPJ:", self.cnpj_input)
        form_layout.addRow("Endereço:", self.address_input)

        # Botões
        self.register_button = QPushButton("Cadastrar")
        self.register_button.setMinimumHeight(45)
        self.register_button.setStyleSheet("""
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
        self.register_button.clicked.connect(self.register_establishment)

        self.back_button = QPushButton("Voltar")
        self.back_button.setMinimumHeight(40)
        self.back_button.setStyleSheet("""
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
        self.back_button.clicked.connect(self.handle_back)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.back_button)

        # Organização no layout principal
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def register_establishment(self):
        name = self.name_input.text().strip()
        cnpj = self.cnpj_input.text().strip()
        address = self.address_input.text().strip()

        if not name or not cnpj or not address:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            user_id = self.screens_controller.auth_controller.get_current_user_id()
            self.establishments_controller.register_establishment(name, cnpj, address, user_id)
            QMessageBox.information(self, "Sucesso", "Estabelecimento cadastrado com sucesso!")
            self.screens_controller.set_screen("establishment_home")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar estabelecimento: {str(e)}")

    def handle_back(self):
        self.screens_controller.set_screen("establishment_home")
