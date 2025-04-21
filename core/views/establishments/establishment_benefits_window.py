from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QListWidget,
    QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt

class EstablishmentBenefitsWindow(QWidget):
    def __init__(self, screens_controller, benefits_controller, establishments_controller):
        super().__init__()
        self.screens_controller = screens_controller
        self.benefits_controller = benefits_controller
        self.establishments_controller = establishments_controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gerenciar Benefícios")
        self.setMinimumSize(800, 600)

        main_layout = QHBoxLayout()
        
        # Form section (left side)
        form_section = QWidget()
        form_layout = QVBoxLayout()
        
        title = QLabel("Cadastrar Novo Benefício")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        form_layout.addWidget(title)

        input_form = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome do benefício")
        input_form.addRow("Nome:", self.name_input)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Descrição do benefício")
        input_form.addRow("Descrição:", self.description_input)

        self.discount_input = QDoubleSpinBox()
        self.discount_input.setRange(0, 100)
        self.discount_input.setSuffix("%")
        self.discount_input.setDecimals(1)
        input_form.addRow("Desconto:", self.discount_input)

        self.min_hours_input = QSpinBox()
        self.min_hours_input.setRange(1, 24)
        self.min_hours_input.setSuffix(" horas")
        input_form.addRow("Horas mínimas:", self.min_hours_input)

        form_layout.addLayout(input_form)

        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Salvar Benefício")
        save_button.clicked.connect(self.save_benefit)
        button_layout.addWidget(save_button)

        back_button = QPushButton("Voltar")
        back_button.clicked.connect(self.handle_back)
        button_layout.addWidget(back_button)

        form_layout.addLayout(button_layout)
        form_section.setLayout(form_layout)

        # List section (right side)
        list_section = QWidget()
        list_layout = QVBoxLayout()

        list_title = QLabel("Benefícios Cadastrados")
        list_title.setAlignment(Qt.AlignCenter)
        list_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        list_layout.addWidget(list_title)

        self.benefits_list = QListWidget()
        self.benefits_list.itemDoubleClicked.connect(self.handle_edit_benefit)
        list_layout.addWidget(self.benefits_list)
        
        list_section.setLayout(list_layout)

        # Add both sections to main layout
        main_layout.addWidget(form_section)
        main_layout.addWidget(list_section)
        
        self.setLayout(main_layout)
        self.load_benefits()

    def save_benefit(self):
        name = self.name_input.text().strip()
        description = self.description_input.text().strip()
        discount_value = self.discount_input.value()
        min_hours = self.min_hours_input.value()

        if not name or not description:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            user_id = self.screens_controller.auth_controller.get_current_user_id()
            establishment = self.establishments_controller.get_establishment_by_user(user_id)
            
            if not establishment:
                QMessageBox.warning(self, "Erro", "Estabelecimento não encontrado.")
                return

            self.benefits_controller.create_benefit(
                name, description, discount_value, min_hours, establishment["id"]
            )
            
            QMessageBox.information(self, "Sucesso", "Benefício cadastrado com sucesso!")
            self.clear_form()
            self.load_benefits()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar benefício: {str(e)}")

    def load_benefits(self):
        try:
            user_id = self.screens_controller.auth_controller.get_current_user_id()
            establishment = self.establishments_controller.get_establishment_by_user(user_id)
            
            if not establishment:
                return

            benefits = self.benefits_controller.get_benefits_by_establishment(establishment["id"])
            
            self.benefits_list.clear()
            if not benefits:
                self.benefits_list.addItem("Nenhum benefício cadastrado")
                return

            for benefit in benefits:
                self.benefits_list.addItem(
                    f"{benefit['name']} - {benefit['discount_value']}% (mín. {benefit['min_hours']}h)"
                )

        except Exception as e:
            print(f"Erro ao carregar benefícios: {e}")

    def clear_form(self):
        self.name_input.clear()
        self.description_input.clear()
        self.discount_input.setValue(0)
        self.min_hours_input.setValue(1)

    def handle_back(self):
        self.screens_controller.set_screen("establishment_home")

    def handle_edit_benefit(self, item):
        # Placeholder: abrir tela de edição do benefício
        QMessageBox.information(self, "Editar Benefício", f"Editar benefício: {item.text()}")