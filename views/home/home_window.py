from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout, QListWidget, QListWidgetItem, QStackedWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from controllers.auth.auth_controller import AuthController
from controllers.screens_controller import ScreensController

class HomeWindow(QWidget):
    def __init__(self, screens_controller: ScreensController, auth_controller: AuthController):
        super().__init__()
        print("Inicializando HomeWindow...")  # Log para depuração
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller  # Adiciona o auth_controller
        self.init_ui()
        
    def init_ui(self) -> None:
        main_layout = QHBoxLayout()
        
        self.menu_list = QListWidget()
        self.menu_list.setFixedWidth(200)
        self.menu_items = [
            {"text": "Meus Veículos", "icon": "car-icon.png", "action": self.show_vehicle_screen},
            {"text": "Status das vagas", "icon": "calendar-icon.png", "action": None},
            {"text": "Histórico", "icon": "history-icon.png", "action": None},
            {"text": "Configurações", "icon": "settings-icon.png", "action": self.show_settings_screen},
            {"text": "Sair", "icon": "logout-icon.png", "action": self.handle_logout}
        ]


        self.populate_menu()

        self.content_stack = QStackedWidget()
        self.dashboard_screen = self.create_dashboard_screen()
        self.content_stack.addWidget(self.dashboard_screen)

        main_layout.addWidget(self.menu_list)
        main_layout.addWidget(self.content_stack)

        self.setLayout(main_layout)

    def populate_menu(self) -> None:
        for item in self.menu_items:
            list_item = QListWidgetItem(QIcon(item["icon"]), item["text"])
            self.menu_list.addItem(list_item)

        self.menu_list.itemClicked.connect(self.handle_menu_click)

    def handle_menu_click(self, item: QListWidgetItem) -> None:
        for menu_item in self.menu_items:
            if menu_item["text"] == item.text() and menu_item["action"]:
                menu_item["action"]()
    

    def create_dashboard_screen(self) -> QWidget:
        dashboard_layout = QVBoxLayout()

        title = QLabel("Atividades recentes")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        dashboard_layout.addWidget(title, alignment=Qt.AlignCenter)

        recent_activitites = QLabel("Aqui serão exibidas as atividades recentes do usuário")
        recent_activitites.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(recent_activitites)

        dashboard_widget = QWidget()
        dashboard_widget.setLayout(dashboard_layout)
        return dashboard_widget
    
    def show_vehicle_screen(self) -> None:
        QMessageBox.information(self, "Veículos", "Tela de veículos em desenvolvimento.")

    def show_settings_screen(self) -> None:
        QMessageBox.information(self, "Configurações", "Tela de configurações em desenvolvimento.")

    def handle_logout(self) -> None:
        self.auth_controller.logout()
        self.screens_controller.set_screen("login")
        QMessageBox.information(self, "Logout", "Você foi desconectado com sucesso.")
        print("Usuário desconectado.")