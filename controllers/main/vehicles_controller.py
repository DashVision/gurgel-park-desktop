from repositories.main.vehicles_repository import VehiclesRepository
from models.main.vehicles import Vehicle
from services.email_service import EmailService
from services.notifications import NotificationService

class VehiclesController:
    def __init__(self, repository, notification_repository):
        self.repository = repository
        self.notification_service = NotificationService(notification_repository)

    def register_vehicle(self, plate, brand, model, year, color, user_id, second_user_email=None):
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

    def get_notifications(self, user_id):
        return self.notification_service.get_notifications(user_id)

    def accept_vehicle_share(self, notification_id, vehicle_id, second_user_id):
        try:
            self.repository.associate_vehicle_to_user(vehicle_id, second_user_id)
            self.notification_service.clear_notification(notification_id)
            print("Solicitação de compartilhamento aceita.")
        except Exception as e:
            print(f"Erro ao aceitar solicitação de compartilhamento: {e}")
            raise

    def reject_vehicle_share(self, notification_id):
        try:
            self.notification_service.clear_notification(notification_id)
            print("Solicitação de compartilhamento rejeitada.")
        except Exception as e:
            print(f"Erro ao rejeitar solicitação de compartilhamento: {e}")
            raise