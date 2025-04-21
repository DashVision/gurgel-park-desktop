from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class EstablishmentBenefitsWindow(QWidget):
    def __init__(self, screens_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gerenciar Benefícios")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()
        title = QLabel("Gerenciar Benefícios")
        layout.addWidget(title)

        add_benefit_button = QPushButton("Adicionar Benefício")
        add_benefit_button.clicked.connect(self.add_benefit)
        layout.addWidget(add_benefit_button)

        self.setLayout(layout)

    def add_benefit(self):
        # Implementar lógica para adicionar benefícios
        pass