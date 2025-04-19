from core.repositories.main.vehicles_repository import VehiclesRepository
from core.models.main.vehicles import Vehicle
from core.services.email_service import EmailService
from core.services.notifications import NotificationService
from core.repositories.auth.user_repository import UserRepository

class VehiclesController:
    def __init__(self, repository, notification_repository, auth_controller, user_repository: UserRepository):
        self.repository = repository
        self.notification_service = NotificationService(notification_repository)
        self.auth_controller = auth_controller
        self.user_repository = user_repository  # Adicionado

    def get_user_vehicles(self, user_id):
        return self.repository.get_vehicles_by_user_id(user_id)

    def register_vehicle(self, plate, brand, model, year, color, user_id, second_user_email=None):
        if not user_id:
            print("Erro: user_id é None. Não é possível cadastrar veículos.")  # Log para depuração
            raise ValueError("Usuário não está logado.")

        try:
            vehicle = Vehicle(plate=plate, brand=brand, model=model, year=year, color=color, user_id=user_id)
            vehicle_id = self.repository.create_vehicle(vehicle)

            if second_user_email:
                second_user = self.repository.get_user_by_email(second_user_email)
                if second_user:
                    message = f"O usuário {second_user_email} solicitou compartilhar o veículo {plate}."
                    self.notification_service.add_notification(second_user.id, vehicle_id, message)
                else:
                    raise ValueError("Segundo usuário não encontrado.")

            return vehicle_id
        except Exception as e:
            print(f"Erro ao registrar veículo: {e}")
            raise

    def accept_vehicle_share(self, notification_id, vehicle_id, second_user_id):
        try:
            # Verifica se o veículo já está compartilhado com o usuário
            if self.repository.is_vehicle_shared_with_user(vehicle_id, second_user_id):
                raise ValueError("O veículo já está compartilhado com este usuário.")

            # Associa o veículo ao usuário
            self.repository.associate_vehicle_to_user(vehicle_id, second_user_id)

            # Remove a notificação
            self.notification_service.clear_notification(notification_id)

            # Notifica o solicitante
            requester = self.user_repository.get_user_by_id(second_user_id)
            vehicle = self.repository.get_vehicle_by_id(vehicle_id)
            message = f"Sua solicitação para compartilhar o veículo {vehicle.plate} foi aceita."
            self.notification_service.add_notification(requester["id"], vehicle.id, message)

            print("Solicitação de compartilhamento aceita e notificação enviada ao solicitante.")
        except Exception as e:
            print(f"Erro ao aceitar solicitação de compartilhamento: {e}")
            raise

    def reject_vehicle_share(self, notification_id):
        try:
            self.notification_service.clear_notification(notification_id)

            # Notifica o solicitante
            notification = self.notification_service.get_notification_by_id(notification_id)
            requester = self.repository.get_user_by_id(notification["user_id"])
            vehicle = self.get_vehicle_by_id(notification["vehicle_id"])
            message = f"Sua solicitação para compartilhar o veículo {vehicle['plate']} foi rejeitada."
            self.notification_service.add_notification(requester["id"], vehicle["id"], message)

            print("Solicitação de compartilhamento rejeitada e notificação enviada ao solicitante.")
        except Exception as e:
            print(f"Erro ao rejeitar solicitação de compartilhamento: {e}")
            raise

    def get_vehicle_by_plate(self, placa):
        return self.repository.get_vehicle_by_plate(placa)

    def update_vehicle(self, vehicle_id, plate, brand, model, year, color):
        vehicle = Vehicle(id=vehicle_id, plate=plate, brand=brand, model=model, year=year, color=color)
        self.repository.update_vehicle(vehicle)

    def delete_vehicle_by_plate(self, placa):
        vehicle = self.repository.get_vehicle_by_credentials(placa)
        if vehicle:
            self.repository.delete_vehicle(vehicle["id"])

    def send_vehicle_share_request(self, plate, email):
        try:
            # Verifica se o veículo existe
            vehicle = self.get_vehicle_by_plate(plate)
            if not vehicle:
                raise ValueError("Veículo não encontrado.")

            # Verifica se o e-mail está cadastrado no sistema
            user = self.auth_controller.repository.get_user_by_email(email)
            if not user:
                raise ValueError("O e-mail fornecido não está cadastrado no sistema.")

            # Verifica se o solicitante está tentando enviar para si mesmo
            current_user_id = self.auth_controller.get_current_user_id()
            if (current_user_id == vehicle["user_id"]):
                raise ValueError("Você não pode solicitar o compartilhamento do seu próprio veículo.")

            # Envia o e-mail de solicitação de compartilhamento
            EmailService.send_vehicle_share_request(email, plate)

            # Busca o usuário portador do veículo
            owner = self.auth_controller.repository.get_user_by_id(vehicle["user_id"])
            if not owner:
                raise ValueError("Usuário portador do veículo não encontrado.")

            # Registra a notificação para o portador do veículo
            message = f"O usuário {self.auth_controller.current_email} solicitou compartilhar o veículo {plate}."
            self.notification_service.add_notification(owner["id"], vehicle["id"], message)

            print(f"Solicitação de compartilhamento enviada para {email} e notificação registrada para o portador do veículo.")
            return "Solicitação enviada com sucesso!"
        except ValueError as e:
            print(f"Erro ao enviar solicitação de compartilhamento: {e}")
            return f"Erro: {e}"
        except Exception as e:
            print(f"Erro inesperado ao enviar solicitação de compartilhamento: {e}")
            return "Erro inesperado ao enviar solicitação."

    def get_shared_users(self, vehicle_id: int) -> list[int]:
        """Obtém os IDs dos usuários com quem o veículo está compartilhado."""
        return self.repository.get_users_by_vehicle_id(vehicle_id)