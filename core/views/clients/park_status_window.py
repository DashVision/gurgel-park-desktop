from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtCore import QDateTime

class StatusWindow(QWidget):
    def __init__(self, screens_controller, parking_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.parking_controller = parking_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Status das Vagas")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        self.title = QLabel("Status das Vagas")
        layout.addWidget(self.title)

        self.spots_list = QListWidget()
        layout.addWidget(self.spots_list)

        button_layout = QHBoxLayout()
        
        self.reserve_button = QPushButton("Reservar Vaga")
        self.reserve_button.clicked.connect(self.reserve_spot)
        button_layout.addWidget(self.reserve_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.handle_back)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.load_spots()

    def load_spots(self):
        self.spots_list.clear()
        user_id = self.screens_controller.auth_controller.get_current_user_id()
        establishment = self.screens_controller.establishments_controller.get_establishment_by_user(user_id)
        if not establishment:
            self.spots_list.addItem("Você ainda não possui estacionamento cadastrado. Cadastre um para visualizar o status das vagas.")
            return

        # Buscar configurações de estacionamento do estabelecimento
        configs = self.screens_controller.parking_controller.get_parking_configurations(establishment["id"])
        if not configs:
            self.spots_list.addItem("Seu estabelecimento ainda não possui configuração de estacionamento cadastrada.")
            return

        # Usa a primeira configuração encontrada
        parking_configuration_id = configs[0]["id"]
        spots = self.parking_controller.get_occupied_spots(parking_configuration_id)

        if not spots:
            self.spots_list.addItem("Nenhuma vaga ocupada no momento.")
            return

        for spot in spots:
            status = "Ocupada" if spot["reserved_until"] else "Disponível"
            self.spots_list.addItem(f"Vaga {spot['spot_number']} - {status}")

    def reserve_spot(self):
        selected_item = self.spots_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Erro", "Selecione uma vaga para reservar.")
            return

        spot_number = int(selected_item.text().split()[1])
        user_id = self.screens_controller.auth_controller.get_current_user_id()
        reserved_until = QDateTime.currentDateTime().addSecs(5 * 3600).toString("yyyy-MM-dd HH:mm:ss")

        try:
            self.parking_controller.reserve_spot(1, user_id, spot_number, reserved_until)
            QMessageBox.information(self, "Sucesso", "Vaga reservada com sucesso!")
            self.load_spots()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao reservar vaga: {str(e)}")

    def handle_back(self):
        user_type = self.screens_controller.auth_controller.get_current_user_type()
        if user_type == "cliente":
            self.screens_controller.set_screen("home")
        else:
            self.screens_controller.set_screen("establishment_home")