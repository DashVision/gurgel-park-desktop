from PyQt5.QtWidgets import QStackedWidget, QWidget
from views.auth.LoginScreen import LoginViews
from views.auth.RegisterScreen import RegisterViews
from views.auth.RecoveryScreen import RecoveryView
from views.auth.SwitchPassowrdScreen import SwitchPasswordView
from views.main.HomeScreen import HomeView
from controllers.main.HomeController import HomeController

class ScreensController:
    def __init__(self):
        self.stacked_widget = QStackedWidget()
        self.login_screen = LoginViews(self)
        self.register_screen = RegisterViews(self)
        self.recovery_screen = RecoveryView(self)
        self.switch_password_screen = None
        self.home_screen = None
        
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.register_screen)
        self.stacked_widget.addWidget(self.recovery_screen)
        
        placeholder1 = QWidget()
        placeholder2 = QWidget()
        self.stacked_widget.addWidget(placeholder1)
        self.stacked_widget.addWidget(placeholder2)
        
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
        
    def switch_to_home(self, user_email):
        home_controller = HomeController()
        self.home_screen = HomeView(home_controller, user_email)
        
        self.stacked_widget.removeWidget(self.stacked_widget.widget(4))
        self.stacked_widget.insertWidget(4, self.home_screen)
        self.stacked_widget.setCurrentWidget(self.home_screen)

    def get_stacked_widget(self):
        return self.stacked_widget