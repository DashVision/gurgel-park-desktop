from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout

class EstablishmentRegisterWindow(QWidget):
    def __init__(self, screens_controller, establishments_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.establishments_controller = establishments_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Cadastro de Estabelecimento")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome do Estabelecimento")
        self.cnpj_input = QLineEdit()
        self.cnpj_input.setPlaceholderText("CNPJ (somente números)")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Endereço")

        form_layout.addRow("Nome:", self.name_input)
        form_layout.addRow("CNPJ:", self.cnpj_input)
        form_layout.addRow("Endereço:", self.address_input)

        self.register_button = QPushButton("Cadastrar")
        self.register_button.clicked.connect(self.register_establishment)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.handle_back)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.back_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
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