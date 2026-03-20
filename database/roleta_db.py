from database.config import DB_PATH
import os
import sqlite3


os.makedirs("data",exist_ok=True)



class DBroleta:
    @staticmethod
    def criar_tabela():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS roleta (
                    user_id INTEGER,
                    server_id INTEGER,   
                       
                    partidas INTEGER DEFAULT 0,
                    mortes INTEGER DEFAULT 0,
                    sobrevivencias INTEGER DEFAULT 0,
                    streak_atual INTEGER DEFAULT 0,
                    melhor_streak INTEGER DEFAULT 0,
                    
                    PRIMARY KEY(user_id, server_id)
        )
        ''')

        conn.commit()
        conn.close()
    @staticmethod
    def garantir_usuario(user_id,server_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM roleta WHERE user_id = ? AND server_id = ?",
            (user_id,server_id)
        )

        resultado = cursor.fetchone()

        if resultado is None:
            cursor.execute(
                "INSERT INTO roleta (user_id,server_id) VALUES (?,?)",
                (user_id, server_id,)              
                )
            conn.commit()
        conn.close()
    @staticmethod
    def registrar_sobrevivencia(user_id,server_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE roleta
            SET 
                partidas = partidas + 1,
                sobrevivencias = sobrevivencias + 1,
                streak_atual = streak_atual + 1
            WHERE user_id = ? and server_id = ?
            """, (user_id,server_id))
        
        cursor.execute("""
            SELECT streak_atual, melhor_streak
            FROM roleta
            WHERE user_id = ? and server_id = ?
            """, (user_id,server_id))
        
        resultado = cursor.fetchone()
        
        if resultado is not None:
            streak_atual, melhor_streak = resultado

            if streak_atual > melhor_streak:
                cursor.execute("""
                UPDATE roleta
                SET melhor_streak = ?
                WHERE user_id = ? AND server_id = ?
                """,(streak_atual,user_id,server_id))

        conn.commit()
        conn.close()
    @staticmethod
    def registrar_morte(user_id,server_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE roleta
            SET 
                partidas = partidas + 1,
                mortes = mortes + 1,
                streak_atual = 0
            WHERE user_id = ? and server_id = ?
            """,(user_id,server_id))
        
        conn.commit()
        conn.close()

    @staticmethod   
    def obter_stats(user_id,server_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT  partidas, mortes, sobrevivencias, streak_atual, melhor_streak
            FROM roleta 
            WHERE user_id = ? AND server_id = ?
        """,(user_id,server_id))

        resultado = cursor.fetchone()

        conn.close()

        return resultado