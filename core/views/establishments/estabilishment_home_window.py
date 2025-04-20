from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon

class EstablishmentHomeWindow(QWidget):
    def __init__(self, screens_controller, auth_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gurgel Park - Estabelecimento")
        self.setMinimumSize(1000, 700)

        self.main_layout = QVBoxLayout()

        self.header_layout = QHBoxLayout()
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon("menu-icon.png"))
        self.menu_button.setFixedSize(40, 40)
        self.menu_button.clicked.connect(self.toggle_sidebar)

        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("settings-icon.png"))
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.clicked.connect(self.show_settings_screen)

        self.header_layout.addWidget(self.menu_button)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.settings_button)

        self.main_layout.addLayout(self.header_layout)
        self.content_layout = QHBoxLayout()

        self.sidebar_layout = QVBoxLayout()
        self.menu_list = QListWidget()  
        self.menu_items = [
            {"text": "Gerenciar meu estabelecimento", "icon": "car-icon.png", "action": self.show_establishment_control_screen},
            {"text": "Gerenciar status das vagas", "icon": "calendar-icon.png", "action": self.show_parking_screen},
            {"text": "Configurações", "icon": "settings-icon.png", "action": self.show_settings_screen},
            {"text": "Sair", "icon": "logout-icon.png", "action": self.handle_logout}
        ]

        self.populate_menu()
        self.sidebar_layout.addWidget(self.menu_list)

        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.sidebar_widget.setMinimumWidth(200)
        self.sidebar_widget.setMaximumWidth(200)

        self.content_stack = QStackedWidget()
        self.dashboard_screen = self.create_dashboard_screen()
        self.content_stack.addWidget(self.dashboard_screen)

        self.content_layout.addWidget(self.sidebar_widget)
        self.content_layout.addWidget(self.content_stack)

        self.main_layout.addLayout(self.content_layout)
        self.setLayout(self.main_layout)

    def populate_menu(self):
        user_type = self.auth_controller.get_current_user_type()

        if user_type == "cliente":
            self.menu_items = [
                {"text": "Meus Veículos", "icon": "car-icon.png", "action": self.show_vehicle_screen},
                {"text": "Status das vagas", "icon": "calendar-icon.png", "action": self.show_status_screen},
                {"text": "Notificações", "icon": "notification-icon.png", "action": self.show_notifications_screen},
                {"text": "Configurações", "icon": "settings-icon.png", "action": self.show_settings_screen},
                {"text": "Sair", "icon": "logout-icon.png", "action": self.handle_logout}
            ]

        elif user_type == "estabelecimento":
            self.menu_items = [
                {"text": "Gerenciar meu estabelecimento", "icon": "car-icon.png", "action": self.show_establishment_control_screen},
                {"text": "Gerenciar status das vagas", "icon": "calendar-icon.png", "action": self.show_parking_screen},
                {"text": "Configurações", "icon": "settings-icon.png", "action": self.show_settings_screen},
                {"text": "Sair", "icon": "logout-icon.png", "action": self.handle_logout}
            ]

        self.menu_list.clear()
        for item in self.menu_items:
            list_item = QListWidgetItem(QIcon(item["icon"]), item["text"])
            self.menu_list.addItem(list_item)
        self.menu_list.itemClicked.connect(self.handle_menu_click)

    def handle_menu_click(self, item: QListWidgetItem):
        for menu_item in self.menu_items:
            if menu_item["text"] == item.text() and menu_item["action"]:
                menu_item["action"]()
    

    def create_dashboard_screen(self):
        dashboard_layout = QVBoxLayout()
        title = QLabel("Atividades Recentes")
        dashboard_layout.addWidget(title)

        recent_activities = QLabel("Nenhuma atividade recente.")
        recent_activities.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(recent_activities)

        dashboard_widget = QWidget()
        dashboard_widget.setLayout(dashboard_layout)
        return dashboard_widget
    
    def toggle_sidebar(self):
        self.is_sidebar_visible = not self.is_sidebar_visible
        target_width = 200 if self.is_sidebar_visible else 0

        animation = QPropertyAnimation(self.sidebar_widget, b"minimumWidth")
        animation.setDuration(250)
        animation.setStartValue(self.sidebar_widget.width())
        animation.setEndValue(target_width)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def show_establishment_control_screen(self):
        self.screens_controller.set_screen("establishment_control")

    def show_parking_screen(self):
        self.screens_controller.set_screen("parking")

    def show_settings_screen(self):
        self.screens_controller.set_screen("settings")

    def handle_logout(self):
        self.auth_controller.logout()
        self.screens_controller.set_screen("login")
        QMessageBox.information(self, "Logout", "Você foi desconectado com sucesso.")