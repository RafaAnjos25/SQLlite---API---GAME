import sqlite3

# DB_PATH = "instance/database copy 2.sqlite"
DB_PATH = "instance/player_tabel.sqlite"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Retorna resultados como dicionários
    return conn

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NxOT NULL,
                senha TEXT NOT NULL,
                time_play DATETIME 
            );
        """)