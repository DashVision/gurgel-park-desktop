from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QSpinBox, QPushButton, QLabel, QMessageBox, QListWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent
from controllers.auth.auth_controller import AuthController
from controllers.screens_controller import ScreensController

class CarRegisterWindow(QWidget):
    def __init__(self, screens_controller, auth_controller, vehicles_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller
        self.vehicles_controller = vehicles_controller
        self.user_id = self.auth_controller.get_current_user_id()
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

        # Lista de veículos cadastrados
        self.vehicles_list = QListWidget()
        self.vehicles_list.setMinimumHeight(200)
        self.main_layout.addWidget(QLabel("Veículos Cadastrados:"))
        self.main_layout.addWidget(self.vehicles_list)

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
        cancel_button.clicked.connect(self.handle_cancel)
        buttons_layout.addWidget(register_button)
        buttons_layout.addWidget(cancel_button)

        self.main_layout.addLayout(buttons_layout)
        self.setLayout(self.main_layout)

        # Carrega os veículos do usuário
        self.load_user_vehicles()

    def handle_cancel(self):
        """Fecha a janela de cadastro."""
        self.close()
        self.screens_controller.set_screen("home")

    def load_user_vehicles(self):
        # Verifica se o usuário está logado
        if not self.auth_controller.is_logged_in():
            self.vehicles_list.clear()
            self.vehicles_list.addItem("Por favor, faça login para visualizar seus veículos.")
            print("Usuário não está logado.")  # Log para depuração
            return

        # Obtém o ID do usuário logado
        self.user_id = self.auth_controller.get_current_user_id()
        if not self.user_id:
            self.vehicles_list.clear()
            self.vehicles_list.addItem("Erro ao carregar usuário logado.")
            print("Erro: user_id é None.")  # Log para depuração
            return

        try:
            # Busca os veículos do usuário
            vehicles = self.vehicles_controller.get_user_vehicles(self.user_id)
            self.vehicles_list.clear()

            # Verifica se o usuário não possui veículos
            if not vehicles:
                self.vehicles_list.addItem("Nenhum veículo cadastrado.")
                print("Nenhum veículo encontrado para o usuário.")  # Log para depuração
                return

            # Exibe os veículos na lista
            for vehicle in vehicles:
                item_text = f"{vehicle.plate} - {vehicle.brand} {vehicle.model} ({vehicle.year})"
                self.vehicles_list.addItem(item_text)
            print(f"Veículos carregados: {len(vehicles)}")  # Log para depuração

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar veículos: {str(e)}")
            print(f"Erro ao carregar veículos: {e}")  # Log para depuração

    def register_vehicle(self):
        self.user_id = self.auth_controller.get_current_user_id()
        if not self.user_id:
            QMessageBox.critical(self, "Erro", "Usuário não está logado. Não é possível cadastrar veículos.")
            return

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
            vehicle_id = self.vehicles_controller.register_vehicle(
                license_plate, brand, model, year, color, self.user_id
            )

            if second_user_email:
                if self.vehicles_controller.send_vehicle_share_request(vehicle_id, second_user_email):
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

            self.placa_input.clear()
            self.marca_input.clear()
            self.modelo_input.clear()
            self.ano_input.setValue(2024)
            self.cor_input.clear()
            self.second_user_email_input.clear()

            QMessageBox.information(self, "Sucesso", "Veículo cadastrado com sucesso!")
            self.load_user_vehicles()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar veículo: {str(e)}")

    def showEvent(self, event: QShowEvent):
        """Carrega os veículos do usuário sempre que a tela for exibida."""
        super().showEvent(event)
        print("Tela de cadastro de veículos exibida. Atualizando lista de veículos...")  # Log para depuração
        self.load_user_vehicles()

