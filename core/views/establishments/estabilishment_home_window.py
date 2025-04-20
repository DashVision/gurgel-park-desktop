from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class EstablishmentHomeWindow(QWidget):
    def __init__(self, screens_controller, auth_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gurgel Park - Estabelecimento")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bem-vindo ao painel do estabelecimento!"))
        self.setLayout(layout)