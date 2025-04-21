from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout

class EstablishmentEditWindow(QWidget):
    def __init__(self, screens_controller, establishments_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.establishments_controller = establishments_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Editar Estabelecimento")
        self.setMinimumSize(400, 300)
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.cnpj_input = QLineEdit()
        self.address_input = QLineEdit()

        layout.addWidget(QLabel("Nome:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("CNPJ:"))
        layout.addWidget(self.cnpj_input)
        layout.addWidget(QLabel("Endereço:"))
        layout.addWidget(self.address_input)

        # Botões Salvar e Cancelar
        btn_layout = QHBoxLayout()
        self.save_button = QPushButton("Salvar Alterações")
        self.save_button.clicked.connect(self.save_changes)
        btn_layout.addWidget(self.save_button)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.handle_return)
        btn_layout.addWidget(self.cancel_button)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_establishment(self, establishment):
        self.establishment = establishment
        self.name_input.setText(establishment["name"])
        self.cnpj_input.setText(establishment["cnpj"])
        self.address_input.setText(establishment["address"])

    def save_changes(self):
        name = self.name_input.text().strip()
        cnpj = self.cnpj_input.text().strip()
        address = self.address_input.text().strip()
        if not name or not cnpj or not address:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
        try:
            self.establishments_controller.update_establishment(self.establishment["id"], name, cnpj, address)
            QMessageBox.information(self, "Sucesso", "Informações atualizadas com sucesso!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar: {e}")

    def showEvent(self, event):
        super().showEvent(event)
        try:
            user_id = self.screens_controller.auth_controller.get_current_user_id()
            establishment = self.establishments_controller.get_establishment_by_user(user_id)
            if establishment:
                self.load_establishment(establishment)
        except Exception:
            pass

    def handle_return(self):
        self.screens_controller.set_screen("establishment_home")
