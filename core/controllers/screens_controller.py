from PyQt5.QtWidgets import QStackedWidget, QApplication, QLabel
import sys

class ScreensController(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.screens = {}

    def add_screen(self, name, widget) -> None:
        index = self.addWidget(widget)
        self.screens[name] = index
        print(f"Tela '{name}' adicionada no índice {index}")
        print(f"Telas atualmente registradas: {list(self.screens.keys())}")  # Log adicional

    def set_screen(self, name) -> None:
        # Lista de telas públicas que não exigem login
        public_screens = ["login", "forgot_password", "register", "confirm_code", "new_password"]

        if name in self.screens:
            # Permite acesso a telas públicas sem verificar login
            if name not in public_screens and not self.is_user_logged_in():
                print("Acesso negado. Usuário não está logado.")
                self.set_screen("login")
                return

            index = self.screens[name]
            print(f"Alternando para a tela: {name} (índice {index})")
            
            # Limpa os campos da tela antes de exibi-la
            widget = self.widget(index)
            if hasattr(widget, "clear_fields"):
                widget.clear_fields()
            
            self.setCurrentIndex(index)
        else:
            print(f"Tela '{name}' não encontrada.")

    def is_user_logged_in(self) -> bool:
        # Verifica se o usuário está logado
        return hasattr(self, "auth_controller") and self.auth_controller.current_email is not None

# Teste isolado do ScreensController
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication, QLabel
    app = QApplication(sys.argv)

    screens_controller = ScreensController()

    # Adicione uma tela de teste
    test_screen = QLabel("Tela de Teste")
    screens_controller.add_screen("test", test_screen)
    screens_controller.set_screen("test")

    screens_controller.show()
    sys.exit(app.exec_())