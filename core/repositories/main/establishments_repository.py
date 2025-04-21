from core.config.database_config import get_connection

class EstablishmentsRepository:
    def __init__(self):
        self.conn = get_connection()

    def create_establishment(self, name, cnpj, address, user_id):
        cursor = self.conn.cursor()
        query = """
            INSERT INTO establishments (name, cnpj, address, user_id)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (name, cnpj, address, user_id))
        self.conn.commit()
        cursor.close()

    def get_establishment_by_user(self, user_id):
        cursor = self.conn.cursor()
        query = "SELECT id, name, cnpj, address FROM establishments WHERE user_id = %s"
        
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "id": result[0],
                "name": result[1],
                "cnpj": result[2],
                "address": result[3],
            }
        
        return None