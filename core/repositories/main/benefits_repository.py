from core.config.database_config import get_connection

class BenefitsRepository:
    def delete_benefit(self, benefit_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM benefits WHERE id = %s"
        cursor.execute(query, (benefit_id,))
        self.conn.commit()
        cursor.close()

    def __init__(self):
        self.conn = get_connection()

    def create_benefit(self, name, description, discount_value, min_hours, establishment_id):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO benefits (name, description, discount_value, min_hours, establishment_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, description, discount_value, min_hours, establishment_id))
        self.conn.commit()
        cursor.close()

    def get_benefits_by_establishment(self, establishment_id):
        cursor = self.conn.cursor()
        query = """
            SELECT id, name, description, discount_value, min_hours 
            FROM benefits 
            WHERE establishment_id = %s
        """
        cursor.execute(query, (establishment_id,))
        results = cursor.fetchall()
        cursor.close()

        benefits = []
        for result in results:
            benefits.append({
                "id": result[0],
                "name": result[1],
                "description": result[2],
                "discount_value": result[3],
                "min_hours": result[4]
            })
        return benefits
