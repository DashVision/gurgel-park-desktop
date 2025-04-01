from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class HomeView(QWidget):
    # Definindo o sinal de logout
    logout_signal = pyqtSignal()

    def __init__(self, controller, user_email):
        super().__init__()
        self.controller = controller
        self.user_email = user_email
        self.is_sidebar_visible = False

        self.main_layout = QVBoxLayout()
        self.content_layout = QHBoxLayout()
        self.sidebar_layout = QVBoxLayout()
        self.panel_layout = QVBoxLayout()
        
        self.user_data = self.controller.get_user_by_email(user_email)
        self.user_name = self.user_data['nome'] if self.user_data else "Usuário"
        
        self.initScreen()

    def initScreen(self):
        self.setWindowTitle("Gurgel Park - Painel Principal")
        self.setWindowIcon(QIcon("views/assets/carro-sedan-na-frente.png"))
        self.setMinimumSize(1000, 700)
        
        self.header_layout = QHBoxLayout()
        
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon("views/assets/icons/menu-icon.png"))
        self.menu_button.setIconSize(QSize(24, 24))
        self.menu_button.setFixedSize(40, 40)
        self.menu_button.setObjectName("menu_button")
        self.menu_button.clicked.connect(self.toggle_sidebar)
        self.header_layout.addWidget(self.menu_button)
        
        self.welcome_text = QLabel(f"Olá {self.user_name}")
        self.welcome_text.setAlignment(Qt.AlignCenter)
        self.welcome_text.setObjectName("welcome_text")
        self.header_layout.addWidget(self.welcome_text, 1)
        
        self.main_layout.addLayout(self.header_layout)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setObjectName("divider")
        self.main_layout.addWidget(divider)
        
        self.setup_sidebar()
    
        self.setup_main_panel()
        
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.sidebar_widget.setFixedWidth(0)
        self.sidebar_widget.setObjectName("sidebar")
        
        self.panel_widget = QWidget()
        self.panel_widget.setLayout(self.panel_layout)
        self.panel_widget.setObjectName("panel")
        
        self.content_layout.addWidget(self.sidebar_widget)
        self.content_layout.addWidget(self.panel_widget)
        
        self.main_layout.addLayout(self.content_layout)
    
        self.setLayout(self.main_layout)
        
        self.setup_styles()
    
    def setup_sidebar(self):
        sidebar_title = QLabel("Menu")
        sidebar_title.setObjectName("sidebar_title")
        self.sidebar_layout.addWidget(sidebar_title)

        # Fazer esses botões aqui do menu funcionar 
        menu_items = [
            {"text": "Meus Veículos", "icon": "car-icon.png"},
            {"text": "Status das vagas", "icon": "calendar-icon.png"},
            {"text": "Histórico", "icon": "history-icon.png"},
            {"text": "Configurações", "icon": "settings-icon.png"},
            {"text": "Sair", "icon": "logout-icon.png"}
        ]
        
        for item in menu_items:
            menu_button = QPushButton(item["text"])
            try:
                menu_button.setIcon(QIcon(f"views/assets/icons/{item['icon']}"))
            except:
                pass

            menu_button.setIconSize(QSize(20, 20))
            menu_button.setObjectName("sidebar_button")
            
            if item["text"] == "Sair":
                menu_button.clicked.connect(self.logout)
                
            self.sidebar_layout.addWidget(menu_button)
        
        self.sidebar_layout.addStretch()
    
    def logout(self):
        reply = QMessageBox.question(
            self, 
            'Confirmação',
            'Deseja realmente sair?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Emite o sinal de logout em vez de fechar a aplicação
            self.logout_signal.emit()
    
    def setup_main_panel(self):
        panel_title = QLabel("Dashboard")
        panel_title.setObjectName("panel_title")
        self.panel_layout.addWidget(panel_title)
        
        cards_grid = QGridLayout()
        info_cards = [
            {"title": "Total de Veículos", "value": "0", "icon": "car-icon.png"},
            {"title": "Reservas Ativas", "value": "0", "icon": "calendar-icon.png"},
            {"title": "Pagamentos", "value": "R$ 0", "icon": "payment-icon.png"},
            {"title": "Pontos Fidelidade", "value": "0", "icon": "loyalty-icon.png"}
        ]
        
        for i, card_data in enumerate(info_cards):
            card = self.create_info_card(card_data)
            row = i // 2
            col = i % 2
            cards_grid.addWidget(card, row, col)
        
        self.panel_layout.addLayout(cards_grid)
        
        activity_label = QLabel("Atividade Recente")
        activity_label.setObjectName("section_title")
        self.panel_layout.addWidget(activity_label)
        
        activity_list = QListWidget()
        activity_list.setObjectName("activity_list")

        # Fazer adicionar itens a lista n sei como
        activity_list.addItem("a")
        activity_list.addItem("b")
        activity_list.addItem("c")
        self.panel_layout.addWidget(activity_list)
        
        self.panel_layout.addStretch()
    
    def create_info_card(self, data):
        card = QWidget()
        card.setObjectName("info_card")
        card.setMinimumHeight(120)
        
        layout = QVBoxLayout()
        
        title = QLabel(data["title"])
        title.setObjectName("card_title")
        
        value = QLabel(data["value"])
        value.setObjectName("card_value")
        
        layout.addWidget(title)
        layout.addWidget(value)
        
        card.setLayout(layout)
        return card
    
    def toggle_sidebar(self):
        self.is_sidebar_visible = not self.is_sidebar_visible
        
        target_width = 250 if self.is_sidebar_visible else 0
        
        self.animation = QPropertyAnimation(self.sidebar_widget, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(self.sidebar_widget.width())
        self.animation.setEndValue(target_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()
    
    def setup_styles(self):
        self.setStyleSheet("""
            /* General Styles */
            QWidget {
                background-color: #f5f5f5;
                color: #333;
                font-family: 'Arial', sans-serif;
            }
            
            /* Header */
            #welcome_text {
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
                padding: 10px;
            }
            
            #menu_button, #profile_button {
                background-color: #4CAF50;
                border-radius: 20px;
                padding: 5px;
                border: none;
            }
            
            #menu_button:hover, #profile_button:hover {
                background-color: #45a049;
            }
            
            #divider {
                background-color: #e0e0e0;
                height: 1px;
                margin: 10px 0;
            }
            
            /* Sidebar */
            #sidebar {
                background-color: #5A6268;
                color: white;
                border-radius: 5px;
                padding: 10px;
                margin-right: 10px;
            }
            
            #sidebar_title {
                font-size: 18px;
                font-weight: bold;
                padding: 10px 0;
                margin-bottom: 10px;
                border-bottom: 1px solid #8a9199;
            }
            
            #sidebar_button {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            
            #sidebar_button:hover {
                background-color: #4CAF50;
                color: white;
            }
            
            /* Panel */
            #panel {
                background-color: white;
                border-radius: 5px;
                padding: 20px;
            }
            
            #panel_title {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
            }
            
            #section_title {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                margin: 20px 0 10px 0;
            }
            
            /* Cards */
            #info_card {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
            }
            
            #card_title {
                font-size: 16px;
                opacity: 0.8;
            }
            
            #card_value {
                font-size: 24px;
                font-weight: bold;
            }
            
            /* Activity List */
            #activity_list {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 10px;
            }
            
            #activity_list::item {
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
            
            #activity_list::item:last-child {
                border-bottom: none;
            }
        """)        