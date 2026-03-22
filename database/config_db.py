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
    def set_channel(server_id,channel_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO server_config (server_id,channel_id) VALUES (?,?)",
            (server_id,channel_id)
        )

        conn.commit()
        conn.close()
    
    @staticmethod
    def get_channel(server_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT channel_id FROM server_config WHERE server_id = ?",
            (server_id,)
        )

        resultado = cursor.fetchone()

        conn.close()
        

    @staticmethod
    def set_prefix(server_id,prefix):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO server_config (server_id,prefix) VALUES (?,?)",
            (server_id,prefix)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_prefix(server_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT prefix FROM server_config WHERE server_id = ?",
            (server_id,)
        )
        resultado = cursor.fetchone()

        conn.close()

        if resultado is None:
            return "$"
        else:
            return resultado[0]
