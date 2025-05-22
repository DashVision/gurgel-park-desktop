class NotificationService:
    def __init__(self, notifications_repository):
        self.notifications_repository = notifications_repository

    def add_notification(self, user_id, vehicle_id, message):
        """Adiciona uma nova notificação."""
        try:
            self.notifications_repository.create_notification(user_id, vehicle_id, message)
            print("Notificação criada com sucesso!")
        except Exception as e:
            print(f"Erro ao criar notificação: {e}")
            raise

    def get_notifications(self, user_id):
        return self.notifications_repository.get_notifications(user_id)

    def clear_notification(self, notification_id):
        self.notifications_repository.delete_notification(notification_id)

    def get_notification_by_id(self, notification_id):
        return self.notifications_repository.get_notification_by_id(notification_id)

    def notify_vehicle_share_status(self, user_id, vehicle_id, status: str):
        """Notifica o usuário sobre o status da solicitação de compartilhamento."""
        try:
            vehicle = self.notifications_repository.get_vehicle_by_id(vehicle_id)
            message = f"Sua solicitação para compartilhar o veículo {vehicle['placa']} foi {status}."
            self.add_notification(user_id, vehicle_id, message)
        except Exception as e:
            print(f"Erro ao notificar status de compartilhamento: {e}")
            raise
