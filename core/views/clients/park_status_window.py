from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox
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

        self.reserve_button = QPushButton("Reservar Vaga")
        self.reserve_button.clicked.connect(self.reserve_spot)
        layout.addWidget(self.reserve_button)

        self.setLayout(layout)
        self.load_spots()

    def load_spots(self):
        self.spots_list.clear()
        parking_configuration_id = 1  # Exemplo: ID da configuração de estacionamento
        spots = self.parking_controller.get_occupied_spots(parking_configuration_id)

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