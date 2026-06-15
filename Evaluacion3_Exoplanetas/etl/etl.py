# etl/etl.py
import pandas as pd
import requests
import sqlite3
import os
import logging
from clasificar import clasificar_planeta

logging.basicConfig(level=logging.INFO)

DB_PATH = os.getenv("DB_PATH", "/data/exoplanets.db")

def extraer_csv():
    """Fuente 1: CSV de la Evaluación 2."""
    logging.info("Extrayendo CSV...")
    df = pd.read_csv("/data/raw/planets_clean.csv")
    return df

def extraer_api():
    """Fuente 2: NASA Exoplanet Archive API."""
    logging.info("Extrayendo API NASA...")
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    query = """
        SELECT pl_name, hostname, discoverymethod, pl_orbper,
            pl_orbsmax, pl_orbeccen, pl_bmassj, pl_radj, pl_dens,
            sy_dist, st_teff, st_mass, st_rad
        FROM pscomppars
        WHERE pl_bmassj IS NOT NULL AND pl_radj IS NOT NULL
    """
    try:
        response = requests.get(url, params={"query": query, "format": "json"}, timeout=30)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        logging.error(f"Error en API: {e}")
        return pd.DataFrame()

def transformar(df_csv, df_api):
    """Transforma y unifica las dos fuentes al esquema de Moira."""
    logging.info("Transformando datos...")

    # --- Transformar CSV ---
    df1 = pd.DataFrame({
        "nombre":                  df_csv.get("pl_name"),
        "estrella":                df_csv.get("pl_hostname"),
        "metodo_descubrimiento":   df_csv.get("pl_discmethod"),
        "mision":                  df_csv.get("discovery_mission"),
        "planetas_en_sistema":     df_csv.get("planets_in_system"),
        "periodo_orbital_dias":    df_csv.get("pl_orbper"),
        "semieje_mayor_au":        df_csv.get("pl_orbsmax"),
        "excentricidad":           df_csv.get("pl_orbeccen"),
        "masa_jup":                df_csv.get("pl_bmassj"),
        "radio_jup":               df_csv.get("pl_radj"),
        "densidad":                df_csv.get("pl_density"),
        "distancia_pc":            df_csv.get("st_dist"),
        "temp_estrella_k":         df_csv.get("st_teff"),
        "masa_estrella":           df_csv.get("st_mass"),
        "radio_estrella":          df_csv.get("st_rad"),
    })

    # --- Transformar API ---
    if not df_api.empty:
        df2 = pd.DataFrame({
            "nombre":                  df_api.get("pl_name"),
            "estrella":                df_api.get("hostname"),
            "metodo_descubrimiento":   df_api.get("discoverymethod"),
            "mision":                  "NASA API",
            "planetas_en_sistema":     None,
            "periodo_orbital_dias":    df_api.get("pl_orbper"),
            "semieje_mayor_au":        df_api.get("pl_orbsmax"),
            "excentricidad":           df_api.get("pl_orbeccen"),
            "masa_jup":                df_api.get("pl_bmassj"),
            "radio_jup":               df_api.get("pl_radj"),
            "densidad":                df_api.get("pl_dens"),
            "distancia_pc":            df_api.get("sy_dist"),
            "temp_estrella_k":         df_api.get("st_teff"),
            "masa_estrella":           df_api.get("st_mass"),
            "radio_estrella":          df_api.get("st_rad"),
        })
        df_unificado = pd.concat([df1, df2], ignore_index=True)
    else:
        df_unificado = df1

    # Eliminar duplicados por nombre
    df_unificado = df_unificado.drop_duplicates(subset=["nombre"])

    # Calcular planet_type
    df_unificado["planet_type"] = df_unificado["radio_jup"].apply(
        lambda r: clasificar_planeta(r) if pd.notna(r) else "Desconocido"
    )

    return df_unificado

def cargar(df, db_path):
    """Fuente 3: Carga en SQLite (la base que lee Moira)."""
    logging.info(f"Cargando en SQLite: {db_path}")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("planets", conn, if_exists="replace", index=False)
    conn.close()
    logging.info(f"Carga completa: {len(df)} planetas guardados.")

if __name__ == "__main__":
    df_csv = extraer_csv()
    df_api = extraer_api()
    df_final = transformar(df_csv, df_api)
    cargar(df_final, DB_PATH)
    logging.info("ETL completado exitosamente.")