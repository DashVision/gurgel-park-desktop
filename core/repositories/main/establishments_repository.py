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
        # Usa cursor buffered para consumir todos os resultados e evitar erro de resultado não lido
        cursor = self.conn.cursor(buffered=True)
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

    def update_establishment(self, establishment_id, name, cnpj, address):
        cursor = self.conn.cursor()
        query = """
            UPDATE establishments
            SET name = %s, cnpj = %s, address = %s
            WHERE id = %s
        """
        cursor.execute(query, (name, cnpj, address, establishment_id))
        self.conn.commit()
        cursor.close()

    def search_establishments(self, query):
        cursor = self.conn.cursor()
        sql = """
            SELECT id, name, cnpj, address FROM establishments
            WHERE name LIKE %s OR address LIKE %s
        """
        param = f"%{query}%"
        cursor.execute(sql, (param, param))
        results = cursor.fetchall()
        cursor.close()
        return [
            {"id": row[0], "name": row[1], "cnpj": row[2], "address": row[3]} for row in results
        ]