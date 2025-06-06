import os
import sys
from PyQt5.QtWidgets import QApplication
from core.application_initializer import initialize_application
from core.utils.os_config import configure_os

def main():
    configure_os()

    app = QApplication(sys.argv)

    screens_controller = initialize_application()
    screens_controller.set_screen("login")
    screens_controller.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()