from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from datetime import datetime
from core.controllers.auth.auth_controller import AuthController
from core.controllers.screens_controller import ScreensController


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

        # Estilo da janela inteira
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial, sans-serif;
            }
        """)

        # Layout principal
        self.main_layout = QVBoxLayout()

        # Cabeçalho
        self.header_layout = QHBoxLayout()

        # Botão de menu
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon("menu-icon.png"))
        self.menu_button.setFixedSize(40, 40)
        self.menu_button.clicked.connect(self.toggle_sidebar)
        self.menu_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Botão de configurações
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("settings-icon.png"))
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.clicked.connect(self.show_settings_screen)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Adicionando botões ao cabeçalho
        self.header_layout.addWidget(self.menu_button)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.settings_button)

        self.main_layout.addLayout(self.header_layout)

        # Layout de conteúdo
        self.content_layout = QHBoxLayout()

        # Menu lateral
        self.sidebar_layout = QVBoxLayout()
        self.menu_list = QListWidget()
        self.menu_list.setStyleSheet("""
            QListWidget {
                background-color: #2c2f38;
                color: white;
                font-size: 14px;
                border: none;
                padding: 0;
            }
            QListWidget::item {
                padding: 15px;
            }
            QListWidget::item:selected {
                background-color: #575757;
            }
        """)

        self.menu_items = [
            {"text": "Meus Veículos", "icon": "car-icon.png", "action": self.show_vehicle_screen},
            {"text": "Status das vagas", "icon": "calendar-icon.png", "action": self.show_status_screen},
            {"text": "Notificações", "icon": "notification-icon.png", "action": self.show_notifications_screen},
            {"text": "Configurações", "icon": "settings-icon.png", "action": self.show_settings_screen},
            {"text": "Sair", "icon": "logout-icon.png", "action": self.handle_logout}
        ]
        self.populate_menu()

        self.sidebar_layout.addWidget(self.menu_list)

        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.sidebar_widget.setMinimumWidth(200)
        self.sidebar_widget.setMaximumWidth(200)
        self.sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #2c2f38;
            }
        """)

        # Stack de conteúdo
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
                {"text": "Gerenciar Estabelecimento", "icon": "building-icon.png", "action": self.show_establishment_screen},
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

        # Título das atividades recentes
        title = QLabel("Atividades Recentes")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                color: #333;
                font-weight: bold;
                margin-bottom: 15px;
            }
        """)
        dashboard_layout.addWidget(title)

        activities = self.get_recent_activites()

        for activity in activities:
            activity_label = QLabel(activity)
            activity_label.setAlignment(Qt.AlignLeft)
            activity_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #666;
                    margin-bottom: 10px;
                }
            """)
            dashboard_layout.addWidget(activity_label)

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
        self.screens_controller.set_screen("status")
    
    def show_notifications_screen(self):
        self.screens_controller.set_screen("notifications")

    def show_settings_screen(self):
        self.screens_controller.set_screen("settings")

    def handle_logout(self):
        self.auth_controller.logout()
        self.screens_controller.set_screen("login")
        QMessageBox.information(self, "Logout", "Você foi desconectado com sucesso.")

    def check_notifications(self):
        """Verifica notificações apenas se o usuário estiver logado."""
        if not self.auth_controller.is_logged_in():
            return  # Sai imediatamente se o usuário não estiver logado

        user_id = self.auth_controller.get_current_user_id()
        if not user_id:
            print("check_notifications: ID do usuário não encontrado. Ignorando.")
            return

        print(f"check_notifications: Verificando notificações para o usuário {user_id}.")
        notifications = self.vehicles_controller.notification_service.get_notifications(user_id)
        if notifications:
            for notification in notifications:
                response = QMessageBox.question(
                    self,
                    "Nova Solicitação",
                    notification["message"],
                    QMessageBox.Yes | QMessageBox.No,
                )
                if response == QMessageBox.Yes:
                    self.vehicles_controller.accept_vehicle_share(
                        notification["id"], notification["vehicle_id"], user_id
                    )
                    QMessageBox.information(self, "Sucesso", "Solicitação aceita.")
                else:
                    self.vehicles_controller.reject_vehicle_share(notification["id"])
                    QMessageBox.information(self, "Rejeitada", "Solicitação rejeitada.")
        else:
            print("check_notifications: Nenhuma notificação encontrada.")

    def showEvent(self, event):
        """Evita verificar notificações se o usuário não estiver logado."""
        super().showEvent(event)
        if not self.auth_controller.is_logged_in():
            return  # Sai do método se o usuário não estiver logado
        
        self.content_stack.removeWidget(self.dashboard_screen)
        self.dashboard_screen = self.create_dashboard_screen()
        self.content_stack.addWidget(self.dashboard_screen)
        self.content_stack.setCurrentWidget(self.dashboard_screen)

        self.check_notifications()

    def get_recent_activites(self):
        activities = []

        if not self.auth_controller.is_logged_in():
            return ["Por favor, faça login para visualizar suas atividades."]
        
        user_id = self.auth_controller.get_current_user_id()
        if not user_id:
            return ["Erro ao recuperar o ID do usuário para carregar atividades."]
        
        try:
            vehicles = self.vehicles_controller.get_user_vehicles(user_id)
            for vehicle in vehicles:
                activities.append(f"Veículo {vehicle.plate} adicionado há {self.time_since(vehicle.created_at)}.")
                print(f"Veículo: {vehicle.plate}, Criado em: {vehicle.created_at}")
    
            notifications = self.vehicles_controller.notification_service.get_notifications(user_id)
            for notification in notifications:
                activities.append(f"Notificação: {notification['message']} recebida há {self.time_since(notification['created_at'])}.")

            if not activities:
                activities.append("Nenhuma atividade recente encontrada.")
        
        except Exception as e:
            print(f"Erro ao recuperar atividades: {e}")

        return activities


    def time_since(self, past_time):
        now = datetime.now()
        delta = now - past_time

        if delta.days > 0:
            return f"{delta.days} dias"
        
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} horas"
        
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minutos"
        
        else:
            return f"{delta.seconds} segundos"