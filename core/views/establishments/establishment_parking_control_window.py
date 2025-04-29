from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget,
    QGridLayout, QMessageBox
)
from PyQt5.QtCore import QTimer, QDateTime
import datetime

class EstablishmentParkingControl(QWidget):
    def __init__(self, screens_controller, parking_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.parking_controller = parking_controller
        self.selected_config = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Controle de Estacionamento")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()

        # Título
        self.title = QLabel("Visualização Aérea das Vagas")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)
        layout.addWidget(self.title)

        # Grid visual das vagas
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_widget.setLayout(self.grid_layout)
        layout.addWidget(self.grid_widget)

        # Botão de atualizar
        update_layout = QHBoxLayout()
        self.update_button = QPushButton("Atualizar")
        self.update_button.setMinimumHeight(45)
        self.update_button.setStyleSheet("""
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
        self.update_button.clicked.connect(self.show_parking_grid)
        update_layout.addWidget(self.update_button)
        layout.addLayout(update_layout)

        # Botão de voltar
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
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.show_parking_grid()

        # Atualização automática a cada 30s
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_parking_grid)
        self.timer.start(30000)

    def open_edit_window(self, establishment):
        self.edit_window = EstablishmentEditWindow(self.screens_controller, self.screens_controller.establishments_controller)
        self.edit_window.load_establishment(establishment)
        self.edit_window.show()

    def show_parking_grid(self):
        self.clear_grid()
        user_id = self.screens_controller.auth_controller.get_current_user_id()
        establishment = self.screens_controller.establishments_controller.get_establishment_by_user(user_id)
        if not establishment:
            self.title.setText("Cadastre um estabelecimento para visualizar as vagas.")
            return

        configs = self.parking_controller.get_parking_configurations(establishment["id"])
        if not configs:
            self.title.setText("Configure o estacionamento para visualizar as vagas.")
            return
        config = configs[0]
        self.selected_config = config
        rows, cols = config["rows"], config["columns"]
        spots = self.parking_controller.get_occupied_spots(config["id"])
        occupied = {spot["spot_number"]: spot for spot in spots}
        for i in range(rows):
            for j in range(cols):
                spot_num = i * cols + j + 1
                btn = QPushButton(str(spot_num))
                if spot_num in occupied:
                    spot = occupied[spot_num]
                    reserved_until = spot.get("reserved_until")
                    # Calcula tempo restante
                    if reserved_until:
                        try:
                            dt_until = datetime.datetime.strptime(reserved_until, "%Y-%m-%d %H:%M:%S")
                            now = datetime.datetime.now()
                            delta = dt_until - now
                            if delta.total_seconds() > 0:
                                tempo_restante = str(delta).split('.')[0]  # HH:MM:SS
                            else:
                                tempo_restante = "Expirada"
                        except Exception:
                            tempo_restante = "-"
                    else:
                        tempo_restante = "-"
                    btn.setStyleSheet("background-color: #c0392b; color: white;")
                    btn.setText(f"{spot_num}\nOcupada\n{tempo_restante}")
                    btn.setToolTip(f"Cliente: {spot.get('client_name', 'N/A')}\nAté: {reserved_until}")
                    btn.clicked.connect(lambda _, n=spot_num: self.liberate_spot(n))
                else:
                    btn.setStyleSheet("background-color: #27ae60; color: white;")
                    btn.setText(f"{spot_num}\nLivre")
                    btn.setEnabled(False)
                self.grid_layout.addWidget(btn, i, j)

    def clear_grid(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def liberate_spot(self, spot_number):
        if not self.selected_config:
            return
        reply = QMessageBox.question(self, "Liberar Vaga", f"Deseja liberar a vaga {spot_number}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.parking_controller.release_spot(self.selected_config["id"], spot_number)
                QMessageBox.information(self, "Sucesso", f"Vaga {spot_number} liberada!")
                self.show_parking_grid()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao liberar vaga: {str(e)}")

    def handle_back(self):
        self.screens_controller.set_screen("establishment_home")
