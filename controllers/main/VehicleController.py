from models.main.VehicleModel import VehicleModel

class VehicleController:
    def __init__(self) -> None:
        self.vehicle_model = VehicleModel()

    def register_vehicle(self, license_plate: str, brand: str, model: str, year: int, color: str, user_id: int) -> int:
        return self.vehicle_model.vehicle_registrator(license_plate, brand, model, year, color, user_id)

    def get_user_vehicles(self, user_id: int) -> list:
        return self.vehicle_model.get_user_vehicles(user_id)

    def get_vehicle_by_id(self, vehicle_id: int, user_id: int) -> dict:
        return self.vehicle_model.get_vehicle_by_id(vehicle_id, user_id)

    def delete_vehicle(self, vehicle_id: int, user_id: int) -> bool:
        return self.vehicle_model.delete_vehicle(vehicle_id, user_id)

    def get_recent_activities(self, user_id: int, limit: int = 5) -> list:
        return self.vehicle_model.get_recent_activities(user_id, limit)