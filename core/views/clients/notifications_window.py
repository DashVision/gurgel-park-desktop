from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox, QPushButton
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QShowEvent
from core.controllers.auth.auth_controller import AuthController
from core.controllers.screens_controller import ScreensController

class NotificationsWindow(QWidget):
    def __init__(self, vehicles_controller, auth_controller, screens_controller: ScreensController):
        super().__init__()
        self.vehicles_controller = vehicles_controller
        self.auth_controller = auth_controller
        self.screens_controller = screens_controller
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_notifications)
        self.timer.start(15000)  # Atualiza notificações a cada 15s

    def init_ui(self):
        layout = QVBoxLayout()

        # Estilo geral da janela
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial, sans-serif;
            }
        """)

        # Título
        title = QLabel("Notificações")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        # Lista de notificações
        self.notifications_list = QListWidget()
        self.notifications_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #fff;
                padding: 10px;
            }
            QListWidget:item {
                padding: 15px;
                font-size: 16px;
                color: #333;
            }
            QListWidget:item:hover {
                background-color: #f0f0f0;
            }
        """)
        layout.addWidget(self.notifications_list)

        # Botão de voltar
        back_button = QPushButton("Voltar")
        back_button.setMinimumHeight(40)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #d5d5d5;
            }
        """)
        back_button.clicked.connect(self.go_to_home)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def load_notifications(self):
        """Carrega notificações apenas se o usuário estiver logado."""
        self.notifications_list.clear()

        if not self.auth_controller.is_logged_in():
            print("load_notifications: Usuário não está logado. Ignorando carregamento de notificações.")
            return

        user_id = self.auth_controller.get_current_user_id()
        notifications = self.vehicles_controller.notification_service.get_notifications(user_id)
        if not notifications:
            self.notifications_list.addItem("Nenhuma notificação.")
            return
        for notif in notifications:
            item = QListWidgetItem(f"{notif['message']}\nRecebida em: {notif['created_at']}")
            self.notifications_list.addItem(item)

    def go_to_home(self):
        self.screens_controller.set_screen("home")
