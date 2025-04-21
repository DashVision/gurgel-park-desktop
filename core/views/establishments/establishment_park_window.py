from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QSpinBox, QComboBox, QPushButton, QMessageBox

class EstablishmentPark(QWidget):
    def __init__(self, screens_controller, parking_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.parking_controller = parking_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Configuração do Estacionamento")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.rows_input = QSpinBox()
        self.rows_input.setRange(1, 100)
        self.rows_input.setValue(10)

        self.columns_input = QSpinBox()
        self.columns_input.setRange(1, 100)
        self.columns_input.setValue(10)

        self.spot_type_input = QComboBox()
        self.spot_type_input.addItems(["Normal", "Preferencial", "Reservada"])

        form_layout.addRow("Linhas:", self.rows_input)
        form_layout.addRow("Colunas:", self.columns_input)
        form_layout.addRow("Tipo de Vaga:", self.spot_type_input)

        self.save_button = QPushButton("Salvar Configuração")
        self.save_button.clicked.connect(self.save_parking_configuration)

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def save_parking_configuration(self):
        rows = self.rows_input.value()
        columns = self.columns_input.value()
        spot_type = self.spot_type_input.currentText()

        establishment_id = self.screens_controller.auth_controller.get_current_user_id()

        try:
            self.parking_controller.save_parking_configuration(establishment_id, rows, columns, spot_type)
            QMessageBox.information(self, "Sucesso", "Configuração salva com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar configuração: {str(e)}")