from PyQt5.QtWidgets import (QPushButton, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox, QLineEdit, QDialog, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from core.controllers.auth.auth_controller import AuthController
from core.controllers.screens_controller import ScreensController


class SettingsWindow(QWidget):
    def __init__(self, screens_controller, auth_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Configurações")
        self.setMinimumSize(360, 500)
        self.settings_items = [
            {"text": "Alterar Senha", "action": self.change_password},
            {"text": "Alterar Email", "action": self.change_email},
            {"text": "Alterar Tema", "action": self.change_theme},
            {"text": "Logout", "action": self.handle_logout},
            {"text": "Excluir Conta", "action": self.exclude_account},
        ]

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        title = QLabel("Configurações")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)

        # Crie o QListWidget ANTES de popular
        self.settings_list = QListWidget()
        layout.addWidget(self.settings_list)

        self.populate_settings_list()  # Agora pode chamar

        # Botão de voltar (exemplo)
        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.go_to_home)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def populate_settings_list(self):
        for item in self.settings_items:
            list_item = QListWidgetItem(QIcon("core/assets/settings-icon.png"), item["text"])  # Adiciona um ícone genérico
            self.settings_list.addItem(list_item)
        self.settings_list.itemClicked.connect(self.handle_item_click)

    def handle_item_click(self, item: QListWidgetItem):
        for menu_item in self.settings_items:
            if menu_item["text"] == item.text() and menu_item["action"]:
                menu_item["action"]()

    def change_password(self):
        user_id = self.auth_controller.get_current_user_id()
        if not user_id:
            QMessageBox.warning(self, "Erro", "Usuário não está logado.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Alterar Senha")
        dialog.setMinimumSize(400, 200)

        layout = QFormLayout()

        current_password_input = QLineEdit()
        current_password_input.setEchoMode(QLineEdit.Password)
        new_password_input = QLineEdit()
        new_password_input.setEchoMode(QLineEdit.Password)
        confirm_password_input = QLineEdit()
        confirm_password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("Senha Atual:", current_password_input)
        layout.addRow("Nova Senha:", new_password_input)
        layout.addRow("Confirmar Nova Senha:", confirm_password_input)

        save_button = QPushButton("Salvar")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_button.clicked.connect(lambda: self.handle_save_password(
            dialog, current_password_input.text(), new_password_input.text(), confirm_password_input.text()
        ))

        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #d5d5d5;
            }
        """)
        cancel_button.clicked.connect(dialog.reject)

        layout.addRow(save_button, cancel_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def handle_save_password(self, dialog, current_password, new_password, confirm_password):
        if not current_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem.")
            return

        if self.auth_controller.update_password_with_id(self.auth_controller.get_current_user_id(), new_password):
            QMessageBox.information(self, "Sucesso", "Senha alterada com sucesso!")
            dialog.accept()
        else:
            QMessageBox.critical(self, "Erro", "Erro ao alterar a senha.")

    def change_email(self):
        user_id = self.auth_controller.get_current_user_id()
        if not user_id:
            QMessageBox.warning(self, "Erro", "Usuário não está logado.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Alterar Email")
        dialog.setMinimumSize(400, 200)

        layout = QFormLayout()

        new_email_input = QLineEdit()
        new_email_input.setPlaceholderText("Digite o novo email")

        layout.addRow("Novo Email:", new_email_input)

        save_button = QPushButton("Salvar")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_button.clicked.connect(lambda: self.handle_save_email(dialog, new_email_input.text()))
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #d5d5d5;
            }
        """)
        cancel_button.clicked.connect(dialog.reject)

        layout.addRow(save_button, cancel_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def handle_save_email(self, dialog, new_email):
        if not new_email:
            QMessageBox.warning(self, "Erro", "O campo de email não pode estar vazio.")
            return

        try:
            self.auth_controller.repository.update_user_email(self.auth_controller.get_current_user_id(), new_email)
            QMessageBox.information(self, "Sucesso", "Email alterado com sucesso!")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao alterar o email: {str(e)}")

    def change_theme(self):
        QMessageBox.information(self, "Alterar Tema", "Funcionalidade de alteração de tema ainda não implementada.")

    def handle_logout(self):
        self.auth_controller.logout()
        self.screens_controller.set_screen("login")
        QMessageBox.information(self, "Logout", "Você foi desconectado com sucesso.")

    def exclude_account(self):
        user_id = self.auth_controller.get_current_user_id()
        if not user_id:
            QMessageBox.warning(self, "Erro", "Usuário não está logado.")
            return

        confirmation = QMessageBox.question(
            self,
            "Excluir Conta",
            "Você tem certeza que deseja excluir sua conta? Esta ação não pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
            self.auth_controller.repository.delete_user(user_id)
            self.auth_controller.logout()
            self.screens_controller.set_screen("login")
            QMessageBox.information(self, "Conta Excluída", "Sua conta foi excluída com sucesso.")

    def go_to_home(self):
        user_type = self.auth_controller.get_current_user_type()
        if user_type == "cliente":
            self.screens_controller.set_screen("home")
        elif user_type == "estabelecimento":
            self.screens_controller.set_screen("establishment_home")
        else:
            QMessageBox.warning(self, "Erro", "Tipo de usuário desconhecido. Redirecionando para login.")
            self.screens_controller.set_screen("login")
