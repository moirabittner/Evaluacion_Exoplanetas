# Pruebas de la API - Moira
# Arman una base chica de prueba y revisan que los endpoints respondan bien.
import os
import sqlite3
import sys
import pandas as pd
import pytest
from fastapi.testclient import TestClient

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "api"))


@pytest.fixture(scope="module")
def cliente(tmp_path_factory):
    bd = tmp_path_factory.mktemp("data") / "test.db"
    df = pd.DataFrame({
        "nombre": ["A b", "B c", "C d"],
        "estrella": ["A", "B", "C"],
        "mision": ["Kepler", "K2", "Kepler"],
        "masa_jup": [1.0, 0.5, 2.0],
        "radio_jup": [0.10, 0.20, 0.35],
        "periodo_orbital_dias": [10.0, 20.0, 30.0],
        "planet_type": ["Rocoso", "Neptuniano", "Gigante Gaseoso"],
    })
    conn = sqlite3.connect(bd)
    df.to_sql("planets", conn, index=False)
    conn.close()
    os.environ["DB_PATH"] = str(bd)
    import importlib, database, main
    importlib.reload(database)
    importlib.reload(main)
    return TestClient(main.app)


def test_salud(cliente):
    assert cliente.get("/salud").json() == {"estado": "ok"}


def test_estadisticas(cliente):
    r = cliente.get("/estadisticas").json()
    assert r["total_planetas"] == 3
    assert len(r["por_tipo"]) == 3


def test_listar_y_filtrar(cliente):
    assert cliente.get("/planetas").json()["total"] == 3
    r = cliente.get("/planetas", params={"tipo": "Rocoso"}).json()
    assert r["total"] == 1 and r["planetas"][0]["nombre"] == "A b"


def test_detalle_y_404(cliente):
    assert cliente.get("/planetas/A b").json()["planet_type"] == "Rocoso"
    assert cliente.get("/planetas/NoExiste").status_code == 404


def test_tipo_invalido(cliente):
    assert cliente.get("/planetas", params={"tipo": "xx"}).status_code == 400
