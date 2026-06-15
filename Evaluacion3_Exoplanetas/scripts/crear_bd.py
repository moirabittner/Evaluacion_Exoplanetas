# crear_bd.py - Moira
# Carga el CSV de planetas en una base de datos SQLite y le agrega la
# columna planet_type (clasificacion) segun el radio del planeta.
# Lo uso para tener datos de prueba mientras Nicolas termina el ETL.

import os
import sqlite3
import pandas as pd

# Umbrales del radio (en radios de Jupiter). El radio del dataset esta
# acotado (maximo ~0.42), por eso uso estos cortes.
ROCOSO_MAX = 0.16
NEPTUNO_MAX = 0.28


def clasificar(radio):
    if pd.isna(radio):
        return "Desconocido"
    if radio < ROCOSO_MAX:
        return "Rocoso"
    if radio < NEPTUNO_MAX:
        return "Neptuniano"
    return "Gigante Gaseoso"


def crear(csv_path, db_path):
    df = pd.read_csv(csv_path)

    # Me quedo con las columnas que voy a mostrar y las renombro a espanol.
    columnas = {
        "pl_name": "nombre",
        "pl_hostname": "estrella",
        "pl_discmethod": "metodo_descubrimiento",
        "discovery_mission": "mision",
        "planets_in_system": "planetas_en_sistema",
        "pl_orbper": "periodo_orbital_dias",
        "pl_orbsmax": "semieje_mayor_au",
        "pl_orbeccen": "excentricidad",
        "pl_bmassj": "masa_jup",
        "pl_radj": "radio_jup",
        "pl_density": "densidad",
        "st_dist": "distancia_pc",
        "st_teff": "temp_estrella_k",
        "st_mass": "masa_estrella",
        "st_rad": "radio_estrella",
    }
    datos = df[list(columnas.keys())].rename(columns=columnas).copy()
    datos["planet_type"] = datos["radio_jup"].apply(clasificar)

    print("Filas:", len(datos))
    print(datos["planet_type"].value_counts())

    conn = sqlite3.connect(db_path)
    datos.to_sql("planets", conn, if_exists="replace", index=False)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_planet_type ON planets(planet_type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_nombre ON planets(nombre)")
    conn.commit()
    conn.close()
    print("Base de datos creada:", db_path)


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    crear(os.path.join(base, "data", "planets_clean.csv"),
          os.path.join(base, "data", "exoplanets.db"))
