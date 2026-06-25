import os
import sys
import sqlite3
import requests
from datetime import datetime

# Se recomienda exportar la API Key en el entorno de NetHunter: export TMDB_API_KEY="tu_clave"
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    print("[-] Error: La variable de entorno TMDB_API_KEY no está configurada.")
    sys.exit(1)

def update_watchlist():
    conn = sqlite3.connect('watchlist.db')
    cursor = conn.cursor()
    
    # Obtener los elementos almacenados
    cursor.execute("SELECT tmdb_id, media_type, title FROM watchlist")
    items = cursor.fetchall()
    
    if not items:
        print("[*] No hay elementos en la lista de seguimiento para actualizar.")
        return

    for tmdb_id, media_type, current_title in items:
        # Construir la URL según el tipo de contenido (movie o tv)
        url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # TMDb usa 'title' para películas y 'name' para series
                new_title = data.get('title') if media_type == 'movie' else data.get('name')
                release_date = data.get('release_date') if media_type == 'movie' else data.get('first_air_date')
                
                # Actualizar la información en la base de datos local
                cursor.execute('''
                    UPDATE watchlist 
                    SET title = ?, release_date = ?, last_updated = CURRENT_TIMESTAMP 
                    WHERE tmdb_id = ?
                ''', (new_title, release_date, tmdb_id))
                
                print(f"[+] Actualizado: {new_title} (Fecha: {release_date})")
            else:
                print(f"[-] No se pudo obtener datos para el ID {tmdb_id}. Código de estado: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Error de red al consultar el ID {tmdb_id}: {e}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print(f"[*] Iniciando actualización de TMDb: {datetime.now()}")
    update_watchlist()
