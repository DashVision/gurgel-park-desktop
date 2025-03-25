import sys
from PyQt5.QtWidgets import QApplication
from views.LoginScreen import LoginViews


def main():
    app = QApplication(sys.argv)
    window = LoginViews()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()