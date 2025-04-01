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
        if self.switch_password_screen:
            self.stacked_widget.removeWidget(self.switch_password_screen)
            self.switch_password_screen = None
            
        try:
            if hasattr(self, 'recovery_screen') and self.recovery_screen is not None:
                self.recovery_screen.clearFields()
        except RuntimeError:
            pass
        
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def switch_to_register(self):
        self.stacked_widget.setCurrentWidget(self.register_screen)

    def switch_to_recovery(self):
        try:
            # Remove a tela de recuperação atual do stacked widget
            self.stacked_widget.removeWidget(self.recovery_screen)
            
            # Cria uma nova instância da tela de recuperação
            self.recovery_screen = RecoveryView(self)
            
            # Adiciona a nova tela ao stacked widget na mesma posição (índice 2)
            self.stacked_widget.insertWidget(2, self.recovery_screen)
        except:
            pass
            
        # Muda para a tela de recuperação
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