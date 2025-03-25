from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from controller.ScreensNavigation import ScreensController

class RegisterViews(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QHBoxLayout()
        self.formLayout = QVBoxLayout()

        self.initScreen()

    def initScreen(self):
        self.setWindowTitle("Registro")
        self.setWindowIcon(QIcon("icons\carro-sedan-na-frente.png"))

        self.setFixedSize(1000, 500)
        
    