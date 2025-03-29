from PyQt5.QtWidgets import QStackedWidget
from views.LoginScreen import LoginViews
from views.RegisterScreen import RegisterViews

class ScreensController:
    def __init__(self):
        self.stacked_widget = QStackedWidget()
        self.login_screen = LoginViews(self)
        self.register_screen = RegisterViews(self)
        
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.register_screen)
        
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def switch_to_login(self):
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def switch_to_register(self):
        self.stacked_widget.setCurrentWidget(self.register_screen)

    def get_stacked_widget(self):
        return self.stacked_widget