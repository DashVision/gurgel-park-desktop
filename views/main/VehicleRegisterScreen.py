from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class VehicleRegistrationView(QWidget):
    def __init__(self, controller, user_id):
        super().__init__()
        self.controller = controller
        self.user_id = user_id
        self.is_sidebar_visible = False

        self.main_layout = QVBoxLayout()
        self.content_layout = QHBoxLayout()
        self.sidebar_layout = QVBoxLayout()
        self.panel_layout = QVBoxLayout()

        self.initScreen()

    def initScreen(self):
        self.setWindowTitle("Gurgel Park - Cadastro de Veículo")
        self.setWindowIcon(QIcon("views/assets/carro-sedan-na-frente.png"))
        self.setMinimumSize(1000, 700)

        header_layout = QHBoxLayout()
        
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon("views/assets/icons/menu-icon.png"))
        self.menu_button.setIconSize(QSize(24, 24))
        self.menu_button.setFixedSize(40, 40)
        self.menu_button.setObjectName("menu_button")
        self.menu_button.clicked.connect(self.toggle_sidebar)
        header_layout.addWidget(self.menu_button)

        title = QLabel("Cadastro de Veículo")
        title.setObjectName("page_title")
        header_layout.addWidget(title)
        
        self.main_layout.addLayout(header_layout)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setObjectName("divider")
        self.main_layout.addWidget(divider)

        self.setup_sidebar()
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        self.placa_input = QLineEdit()
        self.placa_input.setPlaceholderText("Ex: ABC1234")
        self.placa_input.setObjectName("input_field")
        self.placa_input.setMaxLength(7)
        
        self.marca_input = QLineEdit()
        self.marca_input.setPlaceholderText("Ex: Toyota")
        self.marca_input.setObjectName("input_field")
        
        self.modelo_input = QLineEdit()
        self.modelo_input.setPlaceholderText("Ex: Corolla")
        self.modelo_input.setObjectName("input_field")
        
        self.ano_input = QSpinBox()
        self.ano_input.setRange(1900, 2025)
        self.ano_input.setValue(2024)
        self.ano_input.setObjectName("input_field")
        
        self.cor_input = QLineEdit()
        self.cor_input.setPlaceholderText("Ex: Preto")
        self.cor_input.setObjectName("input_field")
        
        form_layout.addRow("Placa:", self.placa_input)
        form_layout.addRow("Marca:", self.marca_input)
        form_layout.addRow("Modelo:", self.modelo_input)
        form_layout.addRow("Ano:", self.ano_input)
        form_layout.addRow("Cor:", self.cor_input)
        
        self.panel_layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        register_button = QPushButton("Cadastrar Veículo")
        register_button.setObjectName("primary_button")
        register_button.clicked.connect(self.register_vehicle)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("secondary_button")
        cancel_button.clicked.connect(self.close)
        
        buttons_layout.addWidget(register_button)
        buttons_layout.addWidget(cancel_button)
        
        self.panel_layout.addLayout(buttons_layout)

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

        menu_items = [
            {"text": "Meus Veículos", "icon": "car-icon.png", "action": None},
            {"text": "Status das vagas", "icon": "calendar-icon.png", "action": None},
            {"text": "Histórico", "icon": "history-icon.png", "action": None},
            {"text": "Configurações", "icon": "settings-icon.png", "action": None},
            {"text": "Sair", "icon": "logout-icon.png", "action": self.close}
        ]

        for item in menu_items:
            menu_button = QPushButton(item["text"])
            try:
                menu_button.setIcon(QIcon(f"views/assets/icons/{item['icon']}"))
            except:
                pass

            menu_button.setIconSize(QSize(20, 20))
            menu_button.setObjectName("sidebar_button")

            if item["action"]:
                menu_button.clicked.connect(item["action"])

            self.sidebar_layout.addWidget(menu_button)

        self.sidebar_layout.addStretch()

    def toggle_sidebar(self):
        self.is_sidebar_visible = not self.is_sidebar_visible

        target_width = 250 if self.is_sidebar_visible else 0

        self.animation = QPropertyAnimation(self.sidebar_widget, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(self.sidebar_widget.width())
        self.animation.setEndValue(target_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    def register_vehicle(self):
        license_plate = self.placa_input.text().strip().upper()
        brand = self.marca_input.text().strip()
        model = self.modelo_input.text().strip()
        year = self.ano_input.value()
        color = self.cor_input.text().strip()
        
        if not all([license_plate, brand, model, color]):
            QMessageBox.warning(
                self,
                "Erro",
                "Por favor, preencha todos os campos obrigatórios.",
                QMessageBox.Ok
            )
            return

        try:
            vehicle_id = self.controller.register_vehicle(license_plate, brand, model, year, color, self.user_id)
            
            # Limpar campos após cadastro bem-sucedido
            self.placa_input.clear()
            self.marca_input.clear()
            self.modelo_input.clear()
            self.ano_input.setValue(2024)
            self.cor_input.clear()
            
            # Mostrar mensagem de sucesso
            QMessageBox.information(
                self,
                "Sucesso",
                "Veículo cadastrado com sucesso!",
                QMessageBox.Ok
            )
            
            # Atualizar lista de atividades recentes na tela principal
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, QWidget) and hasattr(widget, 'load_user_activities'):
                    try:
                        # Forçar atualização da lista
                        widget.load_user_activities()
                        print(f"Atividades atualizadas na janela: {widget.windowTitle()}")
                    except Exception as e:
                        print(f"Erro ao atualizar atividades: {str(e)}")
            
            self.close()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao cadastrar veículo: {str(e)}",
                QMessageBox.Ok
            )

    def setup_styles(self):
        self.setStyleSheet("""
            /* General Styles */
            QWidget {
                background-color: #f5f5f5;
                color: #333;
                font-family: 'Arial', sans-serif;
            }

            /* Header */
            #page_title {
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
                padding: 10px;
            }

            #menu_button {
                background-color: #4CAF50;
                border-radius: 20px;
                padding: 5px;
                border: none;
            }

            #menu_button:hover {
                background-color: #45a049;
            }

            /* Divider */
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

            /* Form Labels */
            QLabel {
                font-size: 14px;
                color: #333;
            }

            /* Input Fields */
            #input_field {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
            }

            #input_field:focus {
                border: 2px solid #4CAF50;
            }

            /* Buttons */
            #primary_button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }

            #primary_button:hover {
                background-color: #45a049;
            }

            #secondary_button {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }

            #secondary_button:hover {
                background-color: #da190b;
            }
        """)