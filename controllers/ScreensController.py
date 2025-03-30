from PyQt5.QtWidgets import QStackedWidget, QWidget
from views.LoginScreen import LoginViews
from views.RegisterScreen import RegisterViews
from views.RecoveryScreen import RecoveryView
from views.SwitchPassowrdScreen import SwitchPasswordView

class ScreensController:
    def __init__(self):
        self.stacked_widget = QStackedWidget()
        self.login_screen = LoginViews(self)
        self.register_screen = RegisterViews(self)
        self.recovery_screen = RecoveryView(self)
        self.switch_password_screen = None
        
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.register_screen)
        self.stacked_widget.addWidget(self.recovery_screen)
        
        placeholder = QWidget()
        self.stacked_widget.addWidget(placeholder)
        
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def switch_to_login(self):
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def switch_to_register(self):
        self.stacked_widget.setCurrentWidget(self.register_screen)

    def switch_to_recovery(self):
        self.stacked_widget.setCurrentWidget(self.recovery_screen)

    def switch_to_swpassword(self, email):
        self.switch_password_screen = SwitchPasswordView(self, email)

        self.stacked_widget.removeWidget(self.stacked_widget.widget(3))
        self.stacked_widget.insertWidget(3, self.switch_password_screen)
        self.stacked_widget.setCurrentWidget(self.switch_password_screen)

    def get_stacked_widget(self):
        return self.stacked_widget