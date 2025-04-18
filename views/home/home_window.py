from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QStackedWidget, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from controllers.auth.auth_controller import AuthController
from controllers.screens_controller import ScreensController


class HomeWindow(QWidget):
    def __init__(self, screens_controller: ScreensController, auth_controller: AuthController, vehicles_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller
        self.vehicles_controller = vehicles_controller
        self.is_sidebar_visible = True
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gurgel Park - Dashboard")
        self.setMinimumSize(1000, 700)

        # Layout principal
        self.main_layout = QVBoxLayout()

        # Header com botões
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

        # Conteúdo principal
        self.content_layout = QHBoxLayout()

        # Menu lateral
        self.sidebar_layout = QVBoxLayout()
        self.menu_list = QListWidget()
        self.menu_items = [
            {"text": "Meus Veículos", "icon": "car-icon.png", "action": self.show_vehicle_screen},
            {"text": "Status das vagas", "icon": "calendar-icon.png", "action": self.show_status_screen},
            {"text": "Histórico", "icon": "history-icon.png", "action": self.show_history_screen},
            {"text": "Configurações", "icon": "settings-icon.png", "action": self.show_settings_screen},
            {"text": "Sair", "icon": "logout-icon.png", "action": self.handle_logout}
        ]

        self.populate_menu()
        self.sidebar_layout.addWidget(self.menu_list)

        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.sidebar_widget.setMinimumWidth(200)  # Largura inicial
        self.sidebar_widget.setMaximumWidth(200)  # Largura máxima

        # Painel principal
        self.content_stack = QStackedWidget()
        self.dashboard_screen = self.create_dashboard_screen()
        self.content_stack.addWidget(self.dashboard_screen)

        self.content_layout.addWidget(self.sidebar_widget)
        self.content_layout.addWidget(self.content_stack)

        self.main_layout.addLayout(self.content_layout)
        self.setLayout(self.main_layout)
        self.check_notifications()

    def populate_menu(self):
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
        title.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(title)

        recent_activities = QLabel("Aqui serão exibidas as atividades recentes do usuário.")
        recent_activities.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(recent_activities)

        dashboard_widget = QWidget()
        dashboard_widget.setLayout(dashboard_layout)
        return dashboard_widget

    def toggle_sidebar(self):
        self.is_sidebar_visible = not self.is_sidebar_visible
        target_width = 200 if self.is_sidebar_visible else 0

        # Animação para alterar a largura da barra lateral
        animation = QPropertyAnimation(self.sidebar_widget, b"minimumWidth")
        animation.setDuration(250)
        animation.setStartValue(self.sidebar_widget.width())
        animation.setEndValue(target_width)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def show_vehicle_screen(self):
        self.screens_controller.set_screen("car_register")

    def show_status_screen(self):
        QMessageBox.information(self, "Status das Vagas", "Tela de Status das Vagas em desenvolvimento.")
    
    def show_history_screen(self):
        QMessageBox.information(self, "Histórico", "Tela de Histórico em desenvolvimento.")

    def show_settings_screen(self):
        QMessageBox.information(self, "Configurações", "Tela de Configurações em desenvolvimento.")

    def handle_logout(self):
        self.auth_controller.logout()
        self.screens_controller.set_screen("login")
        QMessageBox.information(self, "Logout", "Você foi desconectado com sucesso.")

    def check_notifications(self):
        # Verifica se o usuário está logado
        if not self.auth_controller.is_logged_in():
            print("Usuário não está logado. Notificações não serão verificadas.")  # Log para depuração
            return

        user_id = self.auth_controller.get_current_user_id()
        if not user_id:
            QMessageBox.warning(self, "Erro", "Usuário não está logado.")
            return

        notifications = self.vehicles_controller.get_notifications(user_id)
        if notifications:
            QMessageBox.information(
                self,
                "Notificações Pendentes",
                f"Você tem {len(notifications)} notificações pendentes.",
            )
        else:
            QMessageBox.information(
                self,
                "Sem Notificações",
                "Você não tem nenhuma notificação pendente."
            )