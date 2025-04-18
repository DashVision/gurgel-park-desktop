from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QSpinBox, QPushButton, QLabel, QMessageBox, QListWidget
)
from PyQt5.QtCore import Qt
from controllers.auth.auth_controller import AuthController
from controllers.screens_controller import ScreensController

class VehicleRegistrationView(QWidget):
    def __init__(self, controller, user_id):
        super().__init__()
        self.controller = controller
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gurgel Park - Cadastro de Veículo")
        self.setMinimumSize(1000, 700)

        # Layout principal
        self.main_layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Cadastro de Veículo")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        self.main_layout.addLayout(header_layout)

        # Formulário de cadastro
        form_layout = QFormLayout()
        self.placa_input = QLineEdit()
        self.placa_input.setPlaceholderText("Ex: ABC1234")
        self.placa_input.setMaxLength(7)

        self.marca_input = QLineEdit()
        self.marca_input.setPlaceholderText("Ex: Toyota")

        self.modelo_input = QLineEdit()
        self.modelo_input.setPlaceholderText("Ex: Corolla")

        self.ano_input = QSpinBox()
        self.ano_input.setRange(1900, 2025)
        self.ano_input.setValue(2024)

        self.cor_input = QLineEdit()
        self.cor_input.setPlaceholderText("Ex: Preto")

        # Campo para adicionar um segundo usuário
        self.second_user_email_input = QLineEdit()
        self.second_user_email_input.setPlaceholderText("Email do segundo usuário (opcional)")

        form_layout.addRow("Placa:", self.placa_input)
        form_layout.addRow("Marca:", self.marca_input)
        form_layout.addRow("Modelo:", self.modelo_input)
        form_layout.addRow("Ano:", self.ano_input)
        form_layout.addRow("Cor:", self.cor_input)
        form_layout.addRow("Segundo Usuário:", self.second_user_email_input)

        self.main_layout.addLayout(form_layout)

        # Botões
        buttons_layout = QHBoxLayout()
        register_button = QPushButton("Cadastrar Veículo")
        register_button.clicked.connect(self.register_vehicle)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(register_button)
        buttons_layout.addWidget(cancel_button)

        self.main_layout.addLayout(buttons_layout)
        self.setLayout(self.main_layout)

    def register_vehicle(self):
        license_plate = self.placa_input.text().strip().upper()
        brand = self.marca_input.text().strip()
        model = self.modelo_input.text().strip()
        year = self.ano_input.value()
        color = self.cor_input.text().strip()
        second_user_email = self.second_user_email_input.text().strip()

        if not all([license_plate, brand, model, color]):
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            # Registra o veículo no banco de dados
            vehicle_id = self.controller.register_vehicle(license_plate, brand, model, year, color, self.user_id)

            # Envia solicitação para o segundo usuário, se fornecido
            if second_user_email:
                if self.controller.send_vehicle_share_request(vehicle_id, second_user_email):
                    QMessageBox.information(
                        self,
                        "Solicitação Enviada",
                        f"Uma solicitação foi enviada para {second_user_email} para compartilhar o veículo.",
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Erro",
                        f"Não foi possível enviar a solicitação para {second_user_email}.",
                    )

            # Limpa os campos após o cadastro
            self.placa_input.clear()
            self.marca_input.clear()
            self.modelo_input.clear()
            self.ano_input.setValue(2024)
            self.cor_input.clear()
            self.second_user_email_input.clear()

            QMessageBox.information(self, "Sucesso", "Veículo cadastrado com sucesso!")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar veículo: {str(e)}")

