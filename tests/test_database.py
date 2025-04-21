from core.config.database_config import get_connection

def test_database_connection():
    conn = get_connection()
    assert conn.is_connected()
    conn.close()