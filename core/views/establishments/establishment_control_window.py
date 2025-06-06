from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt

class EstablishmentControlWindow(QWidget):
    def __init__(self, screens_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Controle de Estabelecimento")
        self.setMinimumSize(800, 600)

        # Estilo da janela inteira
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial, sans-serif;
            }
        """)

        self.main_layout = QVBoxLayout()

        # Menu de navegação
        self.menu_list = QListWidget()
        self.menu_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #ccc;
                border-radius: 8px;
                background-color: #fff;
                font-size: 16px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)

        self.menu_items = [
            {"text": "Editar informações do estabelecimento", "action": self.show_edit_establishment_screen},
            {"text": "Gerenciar meu estacionamento", "action": self.show_manage_parking_screen},
            {"text": "Gerenciar benefícios", "action": self.show_manage_benefits_screen},
            {"text": "Voltar para Home", "action": self.handle_return_to_home}
        ]

        self.populate_menu()
        self.main_layout.addWidget(self.menu_list)

        # Conteúdo (Stacked Widget)
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

    def show_edit_establishment_screen(self):
        """Navega diretamente para a tela de edição das informações do estabelecimento."""
        self.screens_controller.set_screen("establishment_edit")

    def show_manage_parking_screen(self):
        """Navega para a tela de gerenciamento de estacionamento."""
        self.screens_controller.set_screen("establishment_park")

    def show_manage_benefits_screen(self):
        """Navega para a tela de gerenciamento de benefícios."""
        self.screens_controller.set_screen("establishment_benefits")

    def handle_return_to_home(self):
        """Volta para a tela inicial do estabelecimento."""
        self.screens_controller.set_screen("establishment_home")
