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
        if name in self.screens:
            index = self.screens[name]
            print(f"Alternando para a tela: {name} (índice {index})")
            self.setCurrentIndex(index)
        else:
            print(f"Tela '{name}' não encontrada.")

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