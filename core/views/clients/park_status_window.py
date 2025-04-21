from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout,
    QLineEdit, QGridLayout, QMessageBox
)
from PyQt5.QtCore import QDateTime
import datetime

class StatusWindow(QWidget):
    def __init__(self, screens_controller, parking_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.parking_controller = parking_controller
        self.selected_establishment = None
        self.selected_parking_config = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Status das Vagas")
        self.setMinimumSize(800, 600)
        layout = QVBoxLayout()

        # Busca de estabelecimento
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar estabelecimento...")
        self.search_button = QPushButton("🔍")
        self.search_button.clicked.connect(self.search_establishments)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Lista de resultados da busca
        self.establishment_list = QListWidget()
        self.establishment_list.itemClicked.connect(self.handle_establishment_selected)
        layout.addWidget(self.establishment_list)

        # Botão de voltar
        self.back_button = QPushButton("Voltar para Home")
        self.back_button.clicked.connect(self.handle_back)
        layout.addWidget(self.back_button)

        # Label para instruções/status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # Área de visualização aérea das vagas
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_widget.setLayout(self.grid_layout)
        layout.addWidget(self.grid_widget)

        self.setLayout(layout)
        self.load_all_establishments()

    def load_all_establishments(self):
        self.establishment_list.clear()
        self.status_label.setText("")
        self.selected_establishment = None
        self.selected_parking_config = None
        self.clear_grid()
        results = self.screens_controller.establishments_controller.search_establishments("")
        if not results:
            self.status_label.setText("Nenhum estabelecimento cadastrado.")
            return
        for est in results:
            self.establishment_list.addItem(f"{est['name']} - {est['address']}")
        self.found_establishments = results

    def search_establishments(self):
        query = self.search_input.text().strip()
        self.establishment_list.clear()
        self.status_label.setText("")
        self.selected_establishment = None
        self.selected_parking_config = None
        self.clear_grid()

        # Se o campo de busca estiver vazio, mostra todos
        if not query:
            self.load_all_establishments()
            return

        # Busca no controller de estabelecimentos
        results = self.screens_controller.establishments_controller.search_establishments(query)
        if not results:
            self.status_label.setText("Nenhum estabelecimento encontrado.")
            return
        for est in results:
            self.establishment_list.addItem(f"{est['name']} - {est['address']}")
        self.found_establishments = results

    def handle_establishment_selected(self, item):
        idx = self.establishment_list.currentRow()
        est = self.found_establishments[idx]
        self.selected_establishment = est
        self.status_label.setText(f"Estacionamento selecionado: {est['name']}")
        self.show_parking_grid(est)

    def handle_back(self):
        self.screens_controller.set_screen("home")

    def show_parking_grid(self, establishment):
        self.clear_grid()
        configs = self.parking_controller.get_parking_configurations(establishment["id"])
        if not configs:
            self.status_label.setText("Este estabelecimento ainda não possui configuração de estacionamento cadastrada.")
            return
        config = configs[0]
        self.selected_parking_config = config
        rows, cols = config["rows"], config["columns"]
        spots = self.parking_controller.get_occupied_spots(config["id"])
        occupied = {spot["spot_number"]: spot for spot in spots}
        self.cancel_buttons = {}
        for i in range(rows):
            for j in range(cols):
                spot_num = i * cols + j + 1
                btn = QPushButton(str(spot_num))
                if spot_num in occupied:
                    spot = occupied[spot_num]
                    user_id = self.screens_controller.auth_controller.get_current_user_id()
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
                    btn.setToolTip(f"Reservada até: {reserved_until}")
                    if spot.get("user_id") == user_id:
                        btn.setStyleSheet("background-color: #f1c40f; color: black;")
                        btn.setText(f"{spot_num}\nSua Reserva\n{tempo_restante}")
                        btn.clicked.connect(lambda _, n=spot_num: self.cancel_reservation(n))
                        self.cancel_buttons[spot_num] = btn
                    else:
                        btn.setEnabled(False)
                else:
                    btn.setStyleSheet("background-color: #27ae60; color: white;")
                    btn.clicked.connect(lambda _, n=spot_num: self.reserve_spot(n))
                self.grid_layout.addWidget(btn, i, j)

    def cancel_reservation(self, spot_number):
        if not self.selected_parking_config:
            return
        reply = QMessageBox.question(self, "Cancelar Reserva", f"Deseja cancelar a reserva da vaga {spot_number}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                user_id = self.screens_controller.auth_controller.get_current_user_id()
                self.parking_controller.cancel_reservation(self.selected_parking_config["id"], spot_number, user_id)
                QMessageBox.information(self, "Sucesso", f"Reserva da vaga {spot_number} cancelada!")
                self.show_parking_grid(self.selected_establishment)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao cancelar reserva: {str(e)}")

    def reserve_spot(self, spot_number):
        if not self.selected_parking_config or not self.selected_establishment:
            QMessageBox.warning(self, "Erro", "Selecione um estabelecimento e uma configuração de estacionamento.")
            return
        user_id = self.screens_controller.auth_controller.get_current_user_id()
        # Impede múltiplas reservas
        spots = self.parking_controller.get_occupied_spots(self.selected_parking_config["id"])
        for spot in spots:
            if spot.get("user_id") == user_id:
                QMessageBox.warning(self, "Aviso", "Você já possui uma vaga reservada neste estacionamento.")
                return
        reserved_until = QDateTime.currentDateTime().addSecs(5 * 3600).toString("yyyy-MM-dd HH:mm:ss")
        try:
            self.parking_controller.reserve_spot(
                self.selected_parking_config["id"], user_id, spot_number, reserved_until
            )
            QMessageBox.information(self, "Sucesso", f"Vaga {spot_number} reservada por até 5 horas!")
            self.show_parking_grid(self.selected_establishment)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao reservar vaga: {str(e)}")

    def clear_grid(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)