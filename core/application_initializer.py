from core.config.database_initializer import initialize_database  # Importa o inicializador do banco de dados
from core.controllers.screens_controller import ScreensController
from core.controllers.auth.auth_controller import AuthController
from core.controllers.main.vehicles_controller import VehiclesController
from core.repositories.main.vehicles_repository import VehiclesRepository
from core.services.notifications import NotificationService
from core.repositories.main.notifications_repository import NotificationsRepository
from core.repositories.auth.user_repository import UserRepository
from core.views.auth.login_window import LoginWindow
from core.views.auth.forgot_password_window import ForgotPasswordWindow
from core.views.auth.register_window import RegisterWindow
from core.views.auth.new_password_window import NewPasswordWindow
from core.views.auth.confirm_code_window import ConfirmCodeWindow
from core.views.clients.home_window import HomeWindow
from core.views.clients.car_register_window import CarRegisterWindow
from core.views.clients.notifications_window import NotificationsWindow
from core.views.clients.settings_window import SettingsWindow
from core.views.clients.park_status_window import StatusWindow
from core.controllers.main.establishments_controller import EstablishmentsController
from core.repositories.main.establishments_repository import EstablishmentsRepository
from core.views.establishments.estabilishment_home_window import EstablishmentHomeWindow
from core.views.establishments.establishment_control_window import EstablishmentControlWindow
from core.views.establishments.establishment_register_window import EstablishmentRegisterWindow
from core.views.establishments.establishment_benefits_window import EstablishmentBenefitsWindow
from core.views.establishments.establishment_parking_control_window import EstablishmentParkingControl
from core.views.establishments.establishment_park_window import EstablishmentPark
from core.repositories.main.parking_repository import ParkingRepository
from core.controllers.main.parking_controller import ParkingController


def initialize_application():
    try:
        # Inicializa o banco de dados
        print("Inicializando o banco de dados...")
        initialize_database()

        # Instancia o controlador de telas
        print("Instanciando o ScreensController...")
        screens_controller = ScreensController()

        # Instancia o AuthController compartilhado
        print("Instanciando o AuthController...")
        auth_controller = AuthController()

        # Atribui o auth_controller ao screens_controller
        screens_controller.auth_controller = auth_controller

        # Instancia o EstablishmentsController
        print("Instanciando o EstablishmentsController...")
        establishments_repository = EstablishmentsRepository()
        establishments_controller = EstablishmentsController(establishments_repository)

        # Instancia o ParkingController
        print("Instanciando o ParkingController...")
        parking_repository = ParkingRepository()
        parking_controller = ParkingController(parking_repository)

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
            auth_controller=auth_controller,
            user_repository=user_repository
        )

        # Cria as telas e adiciona ao controlador
        print("Criando as telas...")
        login_window = LoginWindow(screens_controller, auth_controller)
        forgot_password_window = ForgotPasswordWindow(screens_controller, auth_controller)
        register_window = RegisterWindow(screens_controller, auth_controller)
        new_password_window = NewPasswordWindow(screens_controller, auth_controller)
        confirm_code_window = ConfirmCodeWindow(screens_controller, auth_controller)
        home_window = HomeWindow(screens_controller, auth_controller, vehicles_controller)
        notifications_window = NotificationsWindow(vehicles_controller, auth_controller, screens_controller)
        settings_window = SettingsWindow(screens_controller, auth_controller)
        status_window = StatusWindow(screens_controller, parking_controller)

        estabilishment_home_window = EstablishmentHomeWindow(screens_controller, auth_controller)
        estabilishment_control_window = EstablishmentControlWindow(screens_controller)
        estabilishment_register_window = EstablishmentRegisterWindow(screens_controller, establishments_controller)
        establishment_benefits_window = EstablishmentBenefitsWindow(screens_controller)
        establishment_parking_control_window = EstablishmentParkingControl(screens_controller, parking_controller)
        establishment_park_window = EstablishmentPark(screens_controller, parking_controller)

        screens_controller.add_screen("login", login_window)
        screens_controller.add_screen("forgot_password", forgot_password_window)
        screens_controller.add_screen("register", register_window)
        screens_controller.add_screen("new_password", new_password_window)
        screens_controller.add_screen("confirm_code", confirm_code_window)
        screens_controller.add_screen("home", home_window)
        screens_controller.add_screen("car_register", CarRegisterWindow(screens_controller, auth_controller, vehicles_controller))
        screens_controller.add_screen("notifications", notifications_window)
        screens_controller.add_screen("settings", settings_window)
        screens_controller.add_screen("establishment_home", estabilishment_home_window)
        screens_controller.add_screen("establishment_control", estabilishment_control_window)
        screens_controller.add_screen("establishment_register", estabilishment_register_window)
        screens_controller.add_screen("establishment_benefits", establishment_benefits_window)
        screens_controller.add_screen("parking_control", establishment_parking_control_window)
        screens_controller.add_screen("establishment_park", establishment_park_window)
        screens_controller.add_screen("status", status_window)

        return screens_controller

    except Exception as e:
        print(f"Erro ao inicializar o aplicativo: {e}")
        raise