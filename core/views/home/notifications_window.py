from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QShowEvent
from core.controllers.auth.auth_controller import AuthController
from core.controllers.screens_controller import ScreensController

class NotificationsWindow(QWidget):
    def __init__(self, vehicles_controller, auth_controller):
        super().__init__()
        self.vehicles_controller = vehicles_controller
        self.auth_controller = auth_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Notificações")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        title = QLabel("Notificações")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        self.notifications_list = QListWidget()
        layout.addWidget(self.notifications_list)

        self.setLayout(layout)

    def load_notifications(self):
        """Carrega notificações apenas se o usuário estiver logado."""
        self.notifications_list.clear()

        if not self.auth_controller.is_logged_in():
            print("load_notifications: Usuário não está logado. Ignorando carregamento de notificações.")
            return

        user_id = self.auth_controller.get_current_user_id()
        if not user_id:
            print("load_notifications: ID do usuário não encontrado. Ignorando.")
            return

        try:
            notifications = self.vehicles_controller.notification_service.get_notifications(user_id)
            if not notifications:
                self.notifications_list.addItem("Nenhuma notificação disponível.")
                return

            for notification in notifications:
                item = QListWidgetItem(notification["message"])
                self.notifications_list.addItem(item)

        except Exception as e:
            print(f"Erro ao carregar notificações: {e}")

    def showEvent(self, event: QShowEvent):
        """Carrega notificações quando a tela for exibida."""
        super().showEvent(event)
        self.load_notifications()