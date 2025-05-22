from core.repositories.main.establishments_repository import EstablishmentsRepository

class EstablishmentsController:
    def __init__(self, repository: EstablishmentsRepository):
        self.repository = repository

    def register_establishment(self, name, cnpj, address, user_id):
        return self.repository.create_establishment(name, cnpj, address, user_id)

    def get_establishment_by_user(self, user_id):
        return self.repository.get_establishment_by_user(user_id)

    def update_establishment(self, establishment_id, name, cnpj, address):
        return self.repository.update_establishment(establishment_id, name, cnpj, address)

    def search_establishments(self, query):
        # Busca flexível por nome ou endereço
        return self.repository.search_establishments(query)