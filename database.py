import sqlite3

def init_db():
    conn = sqlite3.connect('watchlist.db')
    cursor = conn.cursor()
    # Crear tabla para almacenar películas o series
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY,
            tmdb_id INTEGER UNIQUE,
            title TEXT,
            media_type TEXT,
            release_date TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("[*] Base de datos de Watchlist inicializada.")
