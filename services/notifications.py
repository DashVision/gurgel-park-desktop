class NotificationService:
    def __init__(self, repository):
        self.repository = repository

    def add_notification(self, user_id, vehicle_id, message):
        self.repository.create_notification(user_id, vehicle_id, message)

    def get_notifications(self, user_id):
        return self.repository.get_notifications(user_id)

    def clear_notification(self, notification_id):
        self.repository.delete_notification(notification_id)
