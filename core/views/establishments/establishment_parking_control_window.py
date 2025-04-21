from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout

class EstablishmentParkingControl(QWidget):
    def __init__(self, screens_controller, parking_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.parking_controller = parking_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Controle de Estacionamento")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        self.title = QLabel("Vagas Ocupadas")
        layout.addWidget(self.title)

        self.occupied_spots_list = QListWidget()
        layout.addWidget(self.occupied_spots_list)

        button_layout = QHBoxLayout()
        
        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.handle_back)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.load_occupied_spots()

    def load_occupied_spots(self):
        self.occupied_spots_list.clear()
        user_id = self.screens_controller.auth_controller.get_current_user_id()
        establishment = self.screens_controller.establishments_controller.get_establishment_by_user(user_id)
        if not establishment:
            self.occupied_spots_list.addItem("Você ainda não possui estabelecimento cadastrado. Cadastre um para visualizar as vagas ocupadas.")
            return

        # Buscar configurações de estacionamento do estabelecimento
        configs = self.screens_controller.parking_controller.get_parking_configurations(establishment["id"])
        if not configs:
            self.occupied_spots_list.addItem("Seu estabelecimento ainda não possui configuração de estacionamento cadastrada.")
            return

        # Usa a primeira configuração encontrada
        parking_configuration_id = configs[0]["id"]
        spots = self.parking_controller.get_occupied_spots(parking_configuration_id)

        if not spots:
            self.occupied_spots_list.addItem("Nenhuma vaga ocupada no momento.")
        else:
            for spot in spots:
                self.occupied_spots_list.addItem(f"Vaga {spot['id']} - Cliente: {spot['client_name']}")

    def handle_back(self):
        self.screens_controller.set_screen("establishment_home")