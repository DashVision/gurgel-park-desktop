from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget

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

        self.setLayout(layout)
        self.load_occupied_spots()

    def load_occupied_spots(self):
        self.occupied_spots_list.clear()
        establishment_id = self.screens_controller.auth_controller.get_current_user_id()
        spots = self.parking_controller.get_occupied_spots(establishment_id)

        if not spots:
            self.occupied_spots_list.addItem("Nenhuma vaga ocupada no momento.")
        else:
            for spot in spots:
                self.occupied_spots_list.addItem(f"Vaga {spot['id']} - Cliente: {spot['client_name']}")