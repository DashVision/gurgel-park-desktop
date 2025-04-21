class ParkingController:
    def __init__(self, repository):
        self.repository = repository

    def save_parking_configuration(self, establishment_id, rows, columns, spot_type):
        """Salva uma configuração de estacionamento."""
        self.repository.create_parking_configuration(establishment_id, rows, columns, spot_type)

    def get_parking_configurations(self, establishment_id):
        """Obtém as configurações de estacionamento de um estabelecimento."""
        return self.repository.get_parking_configurations(establishment_id)

    def get_occupied_spots(self, establishment_id):
        """Obtém as vagas ocupadas de um estacionamento."""
        return self.repository.get_occupied_spots(establishment_id)

    def reserve_spot(self, parking_configuration_id, user_id, spot_number, reserved_until):
        """Reserva uma vaga para um usuário."""
        self.repository.reserve_spot(parking_configuration_id, user_id, spot_number, reserved_until)

    def release_spot(self, parking_configuration_id, spot_number):
        """Libera uma vaga ocupada."""
        self.repository.release_spot(parking_configuration_id, spot_number)