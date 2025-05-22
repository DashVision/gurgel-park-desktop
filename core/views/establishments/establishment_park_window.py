from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QSpinBox, QComboBox, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt

class EstablishmentPark(QWidget):
    def __init__(self, screens_controller, parking_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.parking_controller = parking_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Configuração do Estacionamento")
        self.setMinimumSize(600, 400)

        # Estilo da janela inteira
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial, sans-serif;
            }
        """)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Linhas de estacionamento
        self.rows_input = QSpinBox()
        self.rows_input.setRange(1, 100)
        self.rows_input.setValue(10)
        self.rows_input.setStyleSheet("""
            QSpinBox {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                background-color: #fff;
            }
            QSpinBox:focus {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)
        
        # Colunas de estacionamento
        self.columns_input = QSpinBox()
        self.columns_input.setRange(1, 100)
        self.columns_input.setValue(10)
        self.columns_input.setStyleSheet("""
            QSpinBox {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                background-color: #fff;
            }
            QSpinBox:focus {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)

        # Tipo de vaga
        self.spot_type_input = QComboBox()
        self.spot_type_input.addItems(["Normal", "Preferencial", "Reservada"])
        self.spot_type_input.setStyleSheet("""
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                background-color: #fff;
            }
            QComboBox:focus {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)

        # Adiciona os campos ao layout
        form_layout.addRow("Linhas:", self.rows_input)
        form_layout.addRow("Colunas:", self.columns_input)
        form_layout.addRow("Tipo de Vaga:", self.spot_type_input)

        # Layout para os botões
        button_layout = QHBoxLayout()
        
        # Botão de salvar configuração
        self.save_button = QPushButton("Salvar Configuração")
        self.save_button.setStyleSheet("""
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
        self.save_button.clicked.connect(self.save_parking_configuration)
        button_layout.addWidget(self.save_button)

        # Botão voltar
        self.back_button = QPushButton("Voltar")
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
        button_layout.addWidget(self.back_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_parking_configuration(self):
        rows = self.rows_input.value()
        columns = self.columns_input.value()
        spot_type = self.spot_type_input.currentText()

        user_id = self.screens_controller.auth_controller.get_current_user_id()
        establishment = self.screens_controller.establishments_controller.get_establishment_by_user(user_id)
        if not establishment:
            QMessageBox.warning(self, "Estabelecimento não encontrado", "Cadastre um estabelecimento antes de configurar o estacionamento.")
            return
        establishment_id = establishment["id"]

        try:
            self.parking_controller.save_parking_configuration(establishment_id, rows, columns, spot_type)
            QMessageBox.information(self, "Sucesso", "Configuração salva com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar configuração: {str(e)}")

    def handle_back(self):
        self.screens_controller.set_screen("establishment_home")
