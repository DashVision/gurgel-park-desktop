from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFormLayout, QLineEdit, QSpinBox, QMessageBox, QListWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent
from core.controllers.auth.auth_controller import AuthController
from core.controllers.screens_controller import ScreensController

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

        # Menu inicial
        self.menu_layout = QVBoxLayout()
        self.menu_widget = QWidget()
        self.menu_widget.setLayout(self.menu_layout)

        menu_label = QLabel("Escolha uma opção:")
        menu_label.setAlignment(Qt.AlignCenter)
        self.menu_layout.addWidget(menu_label)

        my_vehicles_btn = QPushButton("Meus Veículos")
        my_vehicles_btn.clicked.connect(self.show_my_vehicles)
        self.menu_layout.addWidget(my_vehicles_btn)

        new_vehicle_btn = QPushButton("Adicionar Veículo Novo")
        new_vehicle_btn.clicked.connect(self.show_new_vehicle_form)
        self.menu_layout.addWidget(new_vehicle_btn)

        existing_vehicle_btn = QPushButton("Adicionar Veículo Já Cadastrado")
        existing_vehicle_btn.clicked.connect(self.show_existing_vehicle_form)
        self.menu_layout.addWidget(existing_vehicle_btn)

        # Tela de veículos cadastrados
        self.my_vehicles_widget = QWidget()
        self.my_vehicles_layout = QVBoxLayout()
        self.my_vehicles_widget.setLayout(self.my_vehicles_layout)

        self.vehicles_list = QListWidget()
        self.my_vehicles_layout.addWidget(QLabel("Veículos Cadastrados:"))
        self.my_vehicles_layout.addWidget(self.vehicles_list)

        # Botões para alterar e deletar veículos
        self.edit_vehicle_btn = QPushButton("Alterar Veículo")
        self.edit_vehicle_btn.clicked.connect(self.edit_vehicle)
        self.my_vehicles_layout.addWidget(self.edit_vehicle_btn)

        self.delete_vehicle_btn = QPushButton("Deletar Veículo")
        self.delete_vehicle_btn.clicked.connect(self.delete_vehicle)
        self.my_vehicles_layout.addWidget(self.delete_vehicle_btn)

        back_to_menu_btn = QPushButton("Voltar")
        back_to_menu_btn.clicked.connect(self.show_menu)
        self.my_vehicles_layout.addWidget(back_to_menu_btn)

        # Formulário de novo veículo
        self.new_vehicle_widget = QWidget()
        self.new_vehicle_layout = QVBoxLayout()
        self.new_vehicle_widget.setLayout(self.new_vehicle_layout)

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

        form_layout.addRow("Placa:", self.placa_input)
        form_layout.addRow("Marca:", self.marca_input)
        form_layout.addRow("Modelo:", self.modelo_input)
        form_layout.addRow("Ano:", self.ano_input)
        form_layout.addRow("Cor:", self.cor_input)

        self.new_vehicle_layout.addLayout(form_layout)
        register_button = QPushButton("Cadastrar Veículo")
        register_button.clicked.connect(self.register_vehicle)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.show_menu)
        self.new_vehicle_layout.addWidget(register_button)
        self.new_vehicle_layout.addWidget(cancel_button)

        # Formulário de veículo já cadastrado
        self.existing_vehicle_widget = QWidget()
        self.existing_vehicle_layout = QVBoxLayout()
        self.existing_vehicle_widget.setLayout(self.existing_vehicle_layout)

        existing_form_layout = QFormLayout()
        self.existing_plate_input = QLineEdit()
        self.existing_plate_input.setPlaceholderText("Placa do veículo")

        self.existing_email_input = QLineEdit()
        self.existing_email_input.setPlaceholderText("Email do proprietário")

        existing_form_layout.addRow("Placa:", self.existing_plate_input)
        existing_form_layout.addRow("Email:", self.existing_email_input)

        self.existing_vehicle_layout.addLayout(existing_form_layout)
        send_request_button = QPushButton("Enviar Solicitação")
        send_request_button.clicked.connect(self.send_vehicle_share_request)
        back_button = QPushButton("Voltar")
        back_button.clicked.connect(self.show_menu)
        self.existing_vehicle_layout.addWidget(send_request_button)
        self.existing_vehicle_layout.addWidget(back_button)

        # Stacked widget para alternar entre telas
        self.stack = QStackedWidget()
        self.stack.addWidget(self.menu_widget)
        self.stack.addWidget(self.my_vehicles_widget)
        self.stack.addWidget(self.new_vehicle_widget)
        self.stack.addWidget(self.existing_vehicle_widget)

        self.main_layout.addWidget(self.stack)
        self.setLayout(self.main_layout)

        # Carrega os veículos do usuário
        self.load_user_vehicles()

    def show_menu(self):
        self.stack.setCurrentWidget(self.menu_widget)

    def show_my_vehicles(self):
        self.stack.setCurrentWidget(self.my_vehicles_widget)
        self.load_user_vehicles()

    def show_new_vehicle_form(self):
        self.stack.setCurrentWidget(self.new_vehicle_widget)

    def show_existing_vehicle_form(self):
        self.stack.setCurrentWidget(self.existing_vehicle_widget)

    def handle_cancel(self):
        """Fecha a janela de cadastro."""
        self.close()
        self.screens_controller.set_screen("home")

    def load_user_vehicles(self):
        self.vehicles_list.clear()
        if not self.auth_controller.is_logged_in():
            self.vehicles_list.addItem("Por favor, faça login para visualizar seus veículos.")
            print("Usuário não está logado.")  # Log para depuração
            return

        user_id = self.auth_controller.get_current_user_id()
        if not user_id:
            self.vehicles_list.addItem("Erro ao carregar usuário logado.")
            print("Erro: user_id é None.")  # Log para depuração
            return

        try:
            vehicles = self.vehicles_controller.get_user_vehicles(user_id)
            if not vehicles:
                self.vehicles_list.addItem("Nenhum veículo cadastrado.")
                print("Nenhum veículo encontrado para o usuário.")  # Log para depuração
                return

            for vehicle in vehicles:
                item_text = f"{vehicle.plate} - {vehicle.brand} {vehicle.model} ({vehicle.year})"
                self.vehicles_list.addItem(item_text)
            print(f"Veículos carregados: {len(vehicles)}")  # Log para depuração

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar veículos: {str(e)}")
            print(f"Erro ao carregar veículos: {e}")  # Log para depuração

    def register_vehicle(self):
        user_id = self.auth_controller.get_current_user_id()
        if not user_id:
            QMessageBox.critical(self, "Erro", "Usuário não está logado.")
            return

        license_plate = self.placa_input.text().strip().upper()
        brand = self.marca_input.text().strip()
        model = self.modelo_input.text().strip()
        year = self.ano_input.value()
        color = self.cor_input.text().strip()

        if not all([license_plate, brand, model, color]):
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            self.vehicles_controller.register_vehicle(license_plate, brand, model, year, color, user_id)
            QMessageBox.information(self, "Sucesso", "Veículo cadastrado com sucesso!")
            self.show_menu()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar veículo: {str(e)}")

    def send_vehicle_share_request(self):
        plate = self.existing_plate_input.text().strip().upper()
        email = self.existing_email_input.text().strip()

        if not plate or not email:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        # Chama o método do controlador para enviar a solicitação
        result = self.vehicles_controller.send_vehicle_share_request(plate, email) # Consertar aqui

        # Exibe o resultado ao usuário
        if "sucesso" in result.lower():
            QMessageBox.information(self, "Sucesso", result)
            self.show_menu()
        else:
            QMessageBox.critical(self, "Erro", result)

    def edit_vehicle(self):
        """Abre um formulário para editar o veículo selecionado."""
        selected_item = self.vehicles_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um veículo para alterar.")
            return

        vehicle_data = selected_item.text().split(" - ")
        placa = vehicle_data[0]

        vehicle = self.vehicles_controller.get_vehicle_by_plate(placa)
        if not vehicle:
            QMessageBox.critical(self, "Erro", "Erro ao carregar os dados do veículo.")
            return

        # Preenche os campos do formulário com os dados do veículo
        self.placa_input.setText(vehicle["placa"])
        self.marca_input.setText(vehicle["marca"])
        self.modelo_input.setText(vehicle["modelo"])
        self.ano_input.setValue(vehicle["ano"])
        self.cor_input.setText(vehicle["cor"])

        # Alterna para o formulário de novo veículo para edição
        self.show_new_vehicle_form()

        # Remove o botão "Cadastrar Veículo" se ele já estiver presente
        for i in reversed(range(self.new_vehicle_layout.count())):
            widget = self.new_vehicle_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.text() == "Cadastrar Veículo":
                self.new_vehicle_layout.removeWidget(widget)
                widget.deleteLater()

        # Adiciona o botão "Atualizar Veículo"
        self.register_vehicle_btn = QPushButton("Atualizar Veículo")
        self.register_vehicle_btn.clicked.connect(lambda: self.save_vehicle_changes(vehicle["id"]))
        self.new_vehicle_layout.addWidget(self.register_vehicle_btn)

    def save_vehicle_changes(self, vehicle_id):
        """Salva as alterações feitas no veículo."""
        license_plate = self.placa_input.text().strip().upper()
        brand = self.marca_input.text().strip()
        model = self.modelo_input.text().strip()
        year = self.ano_input.value()
        color = self.cor_input.text().strip()

        if not all([license_plate, brand, model, color]):
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            self.vehicles_controller.update_vehicle(vehicle_id, license_plate, brand, model, year, color)
            QMessageBox.information(self, "Sucesso", "Veículo atualizado com sucesso!")
            self.show_menu()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar veículo: {str(e)}")

    def delete_vehicle(self):
        """Deleta o veículo selecionado."""
        selected_item = self.vehicles_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um veículo para deletar.")
            return

        vehicle_data = selected_item.text().split(" - ")
        placa = vehicle_data[0]

        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Tem certeza de que deseja deletar o veículo com placa {placa}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            try:
                self.vehicles_controller.delete_vehicle_by_plate(placa)
                QMessageBox.information(self, "Sucesso", "Veículo deletado com sucesso!")
                self.load_user_vehicles()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao deletar veículo: {str(e)}")

    def showEvent(self, event: QShowEvent):
        """Carrega os veículos do usuário sempre que a tela for exibida."""
        super().showEvent(event)
        print("Tela de cadastro de veículos exibida. Atualizando lista de veículos...")  # Log para depuração
        self.load_user_vehicles()

