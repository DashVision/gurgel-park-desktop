from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QStackedWidget, QMessageBox

class EstablishmentControlWindow(QWidget):
    def __init__(self, screens_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Controle de Estabelecimento")
        self.setMinimumSize(800, 600)

        self.main_layout = QVBoxLayout()
        self.menu_list = QListWidget()
        self.menu_items = [
            {"text": "Cadastro do estabelecimento", "action": self.show_establishment_registration_screen},
            {"text": "Gerenciar meu estacionamento", "action": self.show_manage_parking_screen},
            {"text": "Gerenciar benefícios", "action": self.show_manage_benefits_screen},
            {"text": "Voltar para Home", "action": self.handle_return_to_home}
        ]

        self.populate_menu()
        self.main_layout.addWidget(self.menu_list)

        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)

        self.setLayout(self.main_layout)

    def populate_menu(self):
        for item in self.menu_items:
            list_item = QListWidgetItem(item["text"])
            self.menu_list.addItem(list_item)
        self.menu_list.itemClicked.connect(self.handle_menu_click)

    def handle_menu_click(self, item):
        for menu_item in self.menu_items:
            if menu_item["text"] == item.text() and menu_item["action"]:
                menu_item["action"]()

    def show_establishment_registration_screen(self):
        """Navega para a tela de cadastro do estabelecimento."""
        self.screens_controller.set_screen("establishment_register")

    def show_manage_parking_screen(self):
        """Navega para a tela de gerenciamento de estacionamento."""
        self.screens_controller.set_screen("establishment_park")

    def show_manage_benefits_screen(self):
        """Navega para a tela de gerenciamento de benefícios."""
        self.screens_controller.set_screen("establishment_benefits")

    def handle_return_to_home(self):
        """Volta para a tela inicial do estabelecimento."""
        self.screens_controller.set_screen("establishment_home")