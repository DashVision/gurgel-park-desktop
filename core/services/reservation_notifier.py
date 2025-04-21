import datetime
import time
from core.repositories.main.parking_repository import ParkingRepository
from core.repositories.main.notifications_repository import NotificationsRepository

class ReservationNotifier:
    def __init__(self, parking_repository=None, notifications_repository=None):
        self.parking_repository = parking_repository or ParkingRepository()
        self.notifications_repository = notifications_repository or NotificationsRepository()

    def notify_expiring_reservations(self):
        now = datetime.datetime.now()
        soon = now + datetime.timedelta(minutes=10)
        # Busca todas as reservas que vão expirar nos próximos 10 minutos
        expiring = self.parking_repository.get_reservations_expiring_until(soon)
        for res in expiring:
            user_id = res['user_id']
            spot_number = res['spot_number']
            reserved_until = res['reserved_until']
            message = f"Sua reserva da vaga {spot_number} irá expirar às {reserved_until}."
            self.notifications_repository.create_notification(user_id, None, message)

if __name__ == "__main__":
    notifier = ReservationNotifier()
    while True:
        notifier.notify_expiring_reservations()
        time.sleep(300)  # Checa a cada 5 minutos
