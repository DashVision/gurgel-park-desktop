from core.repositories.main.benefits_repository import BenefitsRepository

class BenefitsController:
    def delete_benefit(self, benefit_id):
        self.repository.delete_benefit(benefit_id)

    def __init__(self, repository: BenefitsRepository):
        self.repository = repository

    def create_benefit(self, name, description, discount_value, min_hours, establishment_id):
        self.repository.create_benefit(name, description, discount_value, min_hours, establishment_id)

    def get_benefits_by_establishment(self, establishment_id):
        return self.repository.get_benefits_by_establishment(establishment_id)
