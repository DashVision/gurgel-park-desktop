from config.database_config import get_connection

class NotificationsRepository:
    def __init__(self):
        print("Inicializando NotificationsRepository...")
        try:
            self.conn = get_connection()
            print("Conexão com o banco de dados estabelecida!")
        except Exception as e:
            print(f"Erro ao inicializar NotificationsRepository: {e}")
            raise

    def __del__(self):
        if self.conn.is_connected():
            print("Fechando conexão com o banco de dados...")
            self.conn.close()

    def create_notification(self, user_id, vehicle_id, message):
        """Cria uma nova notificação no banco de dados."""
        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO notifications (user_id, vehicle_id, message)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (user_id, vehicle_id, message))
            self.conn.commit()
            print("Notificação criada com sucesso!")
        except Exception as e:
            print(f"Erro ao criar notificação: {e}")
            raise
        finally:
            cursor.close()

    def get_notifications(self, user_id):
        """Obtém todas as notificações de um usuário específico."""
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT id, vehicle_id, message, created_at
                FROM notifications
                WHERE user_id = %s
                ORDER BY created_at DESC
            """
            cursor.execute(query, (user_id,))
            notifications = cursor.fetchall()
            print(f"Notificações encontradas: {len(notifications)}")
            return [
                {
                    "id": row[0],
                    "vehicle_id": row[1],
                    "message": row[2],
                    "created_at": row[3],
                }
                for row in notifications
            ]
        except Exception as e:
            print(f"Erro ao buscar notificações: {e}")
            raise
        finally:
            cursor.close()

    def delete_notification(self, notification_id):
        """Remove uma notificação do banco de dados."""
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM notifications WHERE id = %s"
            cursor.execute(query, (notification_id,))
            self.conn.commit()
            print("Notificação removida com sucesso!")
        except Exception as e:
            print(f"Erro ao remover notificação: {e}")
            raise
        finally:
            cursor.close()

    def get_notification_by_id(self, notification_id):
        """Obtém uma notificação específica pelo ID."""
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT id, user_id, vehicle_id, message, created_at
                FROM notifications
                WHERE id = %s
            """
            cursor.execute(query, (notification_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "user_id": row[1],
                    "vehicle_id": row[2],
                    "message": row[3],
                    "created_at": row[4],
                }
            return None
        except Exception as e:
            print(f"Erro ao buscar notificação por ID: {e}")
            raise
        finally:
            cursor.close()