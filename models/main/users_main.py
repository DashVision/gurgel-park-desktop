import mysql.connector
from config import DB_CONFIG

class UsersMain:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor(dictionary=True)
    
    def get_user_data(self, email) -> any:
        if self.cursor is None:
            raise Exception("Erro no cursor")

        query = "SELECT id, nome, email FROM users WHERE email = %s"
        query_values = (email,)

        self.cursor.execute(query, query_values)
        return self.cursor.fetchone() if self.cursor.fetchone() else None

    def __del__(self) -> None:
        if hasattr(self, 'connection') and self.connection is not None:
            if hasattr(self, 'cursor') and self.cursor is not None:
                self.cursor.close()

            self.connection.close()