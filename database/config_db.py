import sqlite3
import os

DB_PATH = os.getenv("DB_PATH","data/roleta.db")

class DBConfig:

    @staticmethod
    def criar_tabela():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS server_config(
            server_id INTEGER PRIMARY KEY,
            channel_id INTEGER,
            prefix TEXT DEFAULT '$'
        )
        ''')

        conn.commit()
        conn.close()

    @staticmethod
    def set_channel():
        pass
    
    @staticmethod
    def get_channel():
        pass

    @staticmethod
    def set_prefix(server_id,prefix):
        pass

    @staticmethod
    def get_prefix(server_id):
        pass