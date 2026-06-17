# Pruebas unitarias de las funciones de transformacion del ETL.
import os
import sys
import pandas as pd
import pytest

# Dejar la carpeta etl/ en el path para poder importar sus funciones.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "etl"))

from clasificar import clasificar_planeta
import etl


def fila_csv(nombre, radio):
    """Arma una fila con los nombres de columna del CSV."""
    return {
        "pl_name": nombre, "pl_hostname": "Estrella", "pl_discmethod": "Transito",
        "discovery_mission": "Kepler", "planets_in_system": 1, "pl_orbper": 10.0,
        "pl_orbsmax": 0.1, "pl_orbeccen": 0.0, "pl_bmassj": 1.0, "pl_radj": radio,
        "pl_density": None, "st_dist": 100.0, "st_teff": 5000.0, "st_mass": 1.0,
        "st_rad": 1.0,
    }


# ---- clasificar_planeta ----
def test_clasificar_rocoso():
    assert clasificar_planeta(0.10) == "Rocoso"

def test_clasificar_neptuniano():
    assert clasificar_planeta(0.20) == "Neptuniano"

def test_clasificar_gigante():
    assert clasificar_planeta(0.40) == "Gigante Gaseoso"

def test_clasificar_limites():
    # Los umbrales son 0.16 y 0.28 (el limite inferior pertenece a la categoria de arriba).
    assert clasificar_planeta(0.16) == "Neptuniano"
    assert clasificar_planeta(0.28) == "Gigante Gaseoso"

def test_clasificar_nulo():
    assert clasificar_planeta(None) == "Desconocido"


# ---- transformar ----
def test_transformar_solo_csv():
    df_csv = pd.DataFrame([fila_csv("A b", 0.10), fila_csv("B c", 0.40)])
    df_api = pd.DataFrame()  # API vacia
    out = etl.transformar(df_csv, df_api)
    # Renombra al esquema de Moira y agrega planet_type
    assert "planet_type" in out.columns
    assert "nombre" in out.columns
    assert list(out["planet_type"]) == ["Rocoso", "Gigante Gaseoso"]

def test_transformar_quita_duplicados():
    # Dos planetas con el mismo nombre deben quedar en uno solo.
    df_csv = pd.DataFrame([fila_csv("A b", 0.10), fila_csv("A b", 0.10)])
    out = etl.transformar(df_csv, pd.DataFrame())
    assert len(out) == 1

def test_transformar_radio_nulo_es_desconocido():
    df_csv = pd.DataFrame([fila_csv("Sin radio", None)])
    out = etl.transformar(df_csv, pd.DataFrame())
    assert out.iloc[0]["planet_type"] == "Desconocido"
