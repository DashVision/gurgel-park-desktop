from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QListWidget,
    QMessageBox
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
        layout = QHBoxLayout()

        # Estilo da janela inteira
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: Arial, sans-serif;
            }
        """)

        # Form section (left side)
        form_section = QWidget()
        form_layout = QVBoxLayout()

        title = QLabel("Cadastrar Novo Benefício")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)
        form_layout.addWidget(title)

        input_form = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome do benefício")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                background-color: #fff;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)
        input_form.addRow("Nome:", self.name_input)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Descrição do benefício")
        self.description_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                background-color: #fff;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)
        input_form.addRow("Descrição:", self.description_input)

        self.discount_input = QDoubleSpinBox()
        self.discount_input.setRange(0, 100)
        self.discount_input.setSuffix("%")
        self.discount_input.setDecimals(1)
        self.discount_input.setStyleSheet("""
            QDoubleSpinBox {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                background-color: #fff;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)
        input_form.addRow("Desconto:", self.discount_input)

        self.min_hours_input = QSpinBox()
        self.min_hours_input.setRange(1, 24)
        self.min_hours_input.setSuffix(" horas")
        self.min_hours_input.setStyleSheet("""
            QSpinBox {
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                background-color: #fff;
            }
            QSpinBox:focus {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)
        input_form.addRow("Horas mínimas:", self.min_hours_input)

        form_layout.addLayout(input_form)

        button_layout = QHBoxLayout()

        save_button = QPushButton("Salvar Benefício")
        save_button.setMinimumHeight(45)
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
        save_button.clicked.connect(self.save_benefit)
        button_layout.addWidget(save_button)

        back_button = QPushButton("Voltar")
        back_button.setMinimumHeight(40)
        back_button.setStyleSheet("""
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
        back_button.clicked.connect(self.handle_back)
        button_layout.addWidget(back_button)

        form_layout.addLayout(button_layout)
        form_section.setLayout(form_layout)

        # List section (right side)
        list_section = QWidget()
        list_layout = QVBoxLayout()

        list_title = QLabel("Benefícios Cadastrados")
        list_title.setAlignment(Qt.AlignCenter)
        list_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        """)
        list_layout.addWidget(list_title)

        self.benefits_list = QListWidget()
        self.benefits_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #ccc;
                border-radius: 8px;
                background-color: #fff;
                padding: 8px;
                font-size: 16px;
            }
        """)
        self.benefits_list.itemDoubleClicked.connect(self.handle_edit_benefit)
        list_layout.addWidget(self.benefits_list)

        delete_button = QPushButton("Excluir Benefício")
        delete_button.setMinimumHeight(45)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        delete_button.clicked.connect(self.handle_delete_benefit)
        list_layout.addWidget(delete_button)

        list_section.setLayout(list_layout)

        # Add both sections to main layout
        layout.addWidget(form_section)
        layout.addWidget(list_section)

        self.setLayout(layout)
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
        benefit = self._find_benefit_by_list_item(item)
        if benefit:
            self.name_input.setText(benefit["name"])
            self.description_input.setText(benefit["description"])
            self.discount_input.setValue(benefit["discount_value"])
            self.min_hours_input.setValue(benefit["min_hours"])
            self.editing_benefit_id = benefit["id"]
        else:
            QMessageBox.warning(self, "Erro", "Não foi possível encontrar os dados do benefício para edição.")

    def handle_delete_benefit(self):
        selected_item = self.benefits_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Erro", "Selecione um benefício para excluir.")
            return
        benefit = self._find_benefit_by_list_item(selected_item)
        if not benefit:
            QMessageBox.warning(self, "Erro", "Não foi possível encontrar os dados do benefício para exclusão.")
            return
        confirm = QMessageBox.question(self, "Excluir Benefício", f"Tem certeza que deseja excluir o benefício '{benefit['name']}'?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                self.benefits_controller.delete_benefit(benefit["id"])
                QMessageBox.information(self, "Sucesso", "Benefício excluído com sucesso!")
                self.clear_form()
                self.load_benefits()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir benefício: {str(e)}")

    def _find_benefit_by_list_item(self, item):
        user_id = self.screens_controller.auth_controller.get_current_user_id()
        establishment = self.establishments_controller.get_establishment_by_user(user_id)
        if not establishment:
            return None
        benefits = self.benefits_controller.get_benefits_by_establishment(establishment["id"])
        for benefit in benefits:
            display_text = f"{benefit['name']} - {benefit['discount_value']}% (mín. {benefit['min_hours']}h)"
            if item.text() == display_text:
                return benefit
        return None
