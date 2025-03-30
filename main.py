import sys
from PyQt5.QtWidgets import QApplication
from controllers.ScreensController import ScreensController

def main():
    app = QApplication(sys.argv)
    controller = ScreensController()
    
    window = controller.get_stacked_widget()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()