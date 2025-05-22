from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QGroupBox, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon

class EstablishmentHomeWindow(QWidget):
    def __init__(self, screens_controller, auth_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.auth_controller = auth_controller
        self.is_sidebar_visible = True
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gurgel Park - Estabelecimento")
        self.setMinimumSize(1000, 700)

        # Estilo da janela inteira
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial;
            }
        """)

        self.main_layout = QVBoxLayout()

        self.header_layout = QHBoxLayout()
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon("core/assets/menu-icon.png"))
        self.menu_button.setFixedSize(40, 40)
        self.menu_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c8c8c8;
            }
        """)
        self.menu_button.clicked.connect(self.toggle_sidebar)

        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("core/assets/settings-icon.png"))
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c8c8c8;
            }
        """)
        self.settings_button.clicked.connect(self.show_settings_screen)

        self.header_layout.addWidget(self.menu_button)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.settings_button)

        self.main_layout.addLayout(self.header_layout)
        self.content_layout = QHBoxLayout()

        self.sidebar_layout = QVBoxLayout()

        # Sidebar com seções em grupos
        # Seção de Cadastro
        cadastro_group = QGroupBox("Cadastro")
        cadastro_group.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border-radius: 8px;
                margin-bottom: 10px;
            }
            QGroupBox:title {
                color: #333;
                font-size: 16px;
            }
        """)
        cadastro_layout = QVBoxLayout()
        btn_cadastrar = QPushButton("Cadastrar Estabelecimento")
        btn_cadastrar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_cadastrar.clicked.connect(self.show_establishment_registration_screen)

        btn_cadastrar_estacionamento = QPushButton("Cadastrar Estacionamento")
        btn_cadastrar_estacionamento.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn_cadastrar_estacionamento.clicked.connect(self.show_park_registration_screen)

        cadastro_layout.addWidget(btn_cadastrar)
        cadastro_layout.addWidget(btn_cadastrar_estacionamento)
        cadastro_group.setLayout(cadastro_layout)
        self.sidebar_layout.addWidget(cadastro_group)

        # Seção de Gerenciamento
        gerenciar_group = QGroupBox("Gerenciamento")
        gerenciar_group.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border-radius: 8px;
                margin-bottom: 10px;
            }
            QGroupBox:title {
                color: #333;
                font-size: 16px;
            }
        """)
        gerenciar_layout = QVBoxLayout()
        btn_meu_est = QPushButton("Alterar informações do estabelecimento")
        btn_meu_est.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        btn_meu_est.clicked.connect(self.show_edit_establishment_screen)
        gerenciar_layout.addWidget(btn_meu_est)

        btn_gerenciar_estacionamento = QPushButton("Gerenciar informações do estacionamento")
        btn_gerenciar_estacionamento.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        btn_gerenciar_estacionamento.clicked.connect(self.show_manage_parking_screen)
        gerenciar_layout.addWidget(btn_gerenciar_estacionamento)

        btn_beneficios = QPushButton("Benefícios")
        btn_beneficios.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        btn_beneficios.clicked.connect(self.show_benefits_screen)
        gerenciar_layout.addWidget(btn_beneficios)

        btn_status = QPushButton("Status das vagas")
        btn_status.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        btn_status.clicked.connect(self.show_parking_screen)
        gerenciar_layout.addWidget(btn_status)

        btn_settings = QPushButton("Configurações")
        btn_settings.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        btn_settings.clicked.connect(self.show_settings_screen)
        gerenciar_layout.addWidget(btn_settings)

        btn_sair = QPushButton("Sair")
        btn_sair.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        btn_sair.clicked.connect(self.handle_logout)
        gerenciar_layout.addWidget(btn_sair)

        gerenciar_group.setLayout(gerenciar_layout)
        self.sidebar_layout.addWidget(gerenciar_group)

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

    def create_dashboard_screen(self):
        dashboard_layout = QVBoxLayout()
        title = QLabel("Atividades Recentes")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)

        recent_activities = QLabel("Nenhuma atividade recente.")
        recent_activities.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(recent_activities)

        dashboard_widget = QWidget()
        dashboard_widget.setLayout(dashboard_layout)
        return dashboard_widget
    
    def toggle_sidebar(self):
        self.is_sidebar_visible = not self.is_sidebar_visible
        target_width = 200 if self.is_sidebar_visible else 0

        # Animar minimumWidth
        self.sidebar_animation = QPropertyAnimation(self.sidebar_widget, b"minimumWidth")
        self.sidebar_animation.setDuration(250)
        self.sidebar_animation.setStartValue(self.sidebar_widget.width())
        self.sidebar_animation.setEndValue(target_width)
        self.sidebar_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.sidebar_animation.start()

        # Animar maximumWidth também
        self.sidebar_animation2 = QPropertyAnimation(self.sidebar_widget, b"maximumWidth")
        self.sidebar_animation2.setDuration(250)
        self.sidebar_animation2.setStartValue(self.sidebar_widget.width())
        self.sidebar_animation2.setEndValue(target_width)
        self.sidebar_animation2.setEasingCurve(QEasingCurve.InOutQuad)
        self.sidebar_animation2.start()

        # Esconder o widget ao final da animação se for fechar
        if not self.is_sidebar_visible:
            def hide_sidebar():
                self.sidebar_widget.setVisible(False)
            self.sidebar_animation2.finished.connect(hide_sidebar)
        else:
            self.sidebar_widget.setVisible(True)

    def show_edit_establishment_screen(self):
        self.screens_controller.set_screen("establishment_edit")

    def show_manage_parking_screen(self):
        self.screens_controller.set_screen("establishment_park")

    def show_benefits_screen(self):
        self.screens_controller.set_screen("establishment_benefits")

    def show_parking_screen(self):
        self.screens_controller.set_screen("parking_control")

    def show_settings_screen(self):
        self.screens_controller.set_screen("settings")

    def handle_logout(self):
        self.auth_controller.logout()
        self.screens_controller.set_screen("login")
        QMessageBox.information(self, "Logout", "Você foi desconectado com sucesso.")

    def show_establishment_registration_screen(self):
        self.screens_controller.set_screen("establishment_register")

    def show_park_registration_screen(self):
        self.screens_controller.set_screen("establishment_park")