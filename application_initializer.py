from controllers.screens_controller import ScreensController
from controllers.auth.auth_controller import AuthController
from controllers.main.vehicles_controller import VehiclesController
from repositories.main.vehicles_repository import VehiclesRepository
from repositories.auth.user_repository import UserRepository
from views.auth.login_window import LoginWindow
from views.auth.forgot_password_window import ForgotPasswordWindow
from views.auth.register_window import RegisterWindow
from views.auth.new_password_window import NewPasswordWindow
from views.auth.confirm_code_window import ConfirmCodeWindow
from views.home.home_window import HomeWindow

def initialize_application():
    print("Inicializando o aplicativo...")  # Log para depuração

    try:
        # Instancia o controlador de telas
        print("Instanciando o ScreensController...")
        screens_controller = ScreensController()

        # Instancia o AuthController compartilhado
        print("Instanciando o AuthController...")
        auth_controller = AuthController()

        # Instancia o VehiclesController
        print("Instanciando o VehiclesController...")
        vehicles_repository = VehiclesRepository()
        user_repository = UserRepository()
        vehicles_controller = VehiclesController(vehicles_repository, user_repository)

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

        screens_controller.auth_controller = auth_controller

        print("Aplicativo inicializado com sucesso!")
        return screens_controller

    except Exception as e:
        print(f"Erro ao inicializar o aplicativo: {e}")
        raise