# Conexion a la base de datos SQLite - Moira
import os
import sqlite3

# La ruta de la base se puede cambiar con una variable de entorno (para Docker).
RUTA_BD = os.getenv("DB_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exoplanets.db"))


def get_conexion():
    if not os.path.exists(RUTA_BD):
        raise FileNotFoundError(
            f"No se encontro la base de datos en {RUTA_BD}. "
            "Corre 'python scripts/crear_bd.py' o levanta el ETL de Nicolas."
        )
    conn = sqlite3.connect(RUTA_BD, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
