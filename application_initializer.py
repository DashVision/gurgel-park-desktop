from controllers.screens_controller import ScreensController
from controllers.auth.auth_controller import AuthController
from controllers.main.vehicles_controller import VehiclesController
from repositories.main.vehicles_repository import VehiclesRepository
from services.notifications import NotificationService
from repositories.main.notifications_repository import NotificationsRepository
from repositories.auth.user_repository import UserRepository
from views.auth.login_window import LoginWindow
from views.auth.forgot_password_window import ForgotPasswordWindow
from views.auth.register_window import RegisterWindow
from views.auth.new_password_window import NewPasswordWindow
from views.auth.confirm_code_window import ConfirmCodeWindow
from views.home.home_window import HomeWindow
from views.home.car_register_window import CarRegisterWindow

def initialize_application():
    try:
        # Instancia o controlador de telas
        print("Instanciando o ScreensController...")
        screens_controller = ScreensController()

        # Instancia o AuthController compartilhado
        print("Instanciando o AuthController...")
        auth_controller = AuthController()

        # Instancia os repositórios
        print("Instanciando os repositórios...")
        vehicles_repository = VehiclesRepository()
        notifications_repository = NotificationsRepository()
        user_repository = UserRepository()

        # Instancia o NotificationService
        notification_service = NotificationService(notifications_repository)

        # Instancia o VehiclesController
        print("Instanciando o VehiclesController...")
        vehicles_controller = VehiclesController(
            repository=vehicles_repository,
            notification_repository=notifications_repository,
            auth_controller=auth_controller
        )

        # Cria as telas e adiciona ao controlador
        print("Criando as telas...")
        login_window = LoginWindow(screens_controller, auth_controller)
        forgot_password_window = ForgotPasswordWindow(screens_controller, auth_controller)
        register_window = RegisterWindow(screens_controller, auth_controller)
        new_password_window = NewPasswordWindow(screens_controller, auth_controller)
        confirm_code_window = ConfirmCodeWindow(screens_controller, auth_controller)
        home_window = HomeWindow(screens_controller, auth_controller, vehicles_controller)

        screens_controller.add_screen("login", login_window)
        screens_controller.add_screen("forgot_password", forgot_password_window)
        screens_controller.add_screen("register", register_window)
        screens_controller.add_screen("new_password", new_password_window)
        screens_controller.add_screen("confirm_code", confirm_code_window)
        screens_controller.add_screen("home", home_window)
        screens_controller.add_screen("car_register", CarRegisterWindow(screens_controller, auth_controller, vehicles_controller))

        screens_controller.auth_controller = auth_controller

        return screens_controller

    except Exception as e:
        print(f"Erro ao inicializar o aplicativo: {e}")
        raise