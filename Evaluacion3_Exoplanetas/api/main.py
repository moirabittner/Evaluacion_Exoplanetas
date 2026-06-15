# API de Exoplanetas con FastAPI - Moira
# Entrega los datos de los planetas (guardados en SQLite) para el dashboard.
# La documentacion Swagger se ve sola en /docs.
#
# Endpoints:
#   GET /salud                 -> dice si la API y la base funcionan
#   GET /planetas              -> lista de planetas con filtros y paginas
#   GET /planetas/{nombre}     -> un planeta puntual
#   GET /estadisticas          -> totales, promedios y conteo por tipo

from typing import Optional
from fastapi import FastAPI, HTTPException, Query

from database import get_conexion
from models import Planeta, PaginaPlanetas, Resumen, ConteoTipo

app = FastAPI(
    title="API Exoplanetas",
    description="API de exoplanetas para el dashboard. Parte de Moira.",
    version="1.0",
)

TIPOS_VALIDOS = {"Rocoso", "Neptuniano", "Gigante Gaseoso", "Desconocido"}


@app.get("/salud")
def salud():
    # Se usa para revisar que la base conecte (util en Docker).
    try:
        conn = get_conexion()
        conn.execute("SELECT 1").fetchone()
        conn.close()
        return {"estado": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="La base de datos no responde")


@app.get("/planetas", response_model=PaginaPlanetas)
def listar_planetas(
    tipo: Optional[str] = Query(None, description="Filtra por tipo de planeta"),
    mision: Optional[str] = Query(None, description="Filtra por mision"),
    pagina: int = Query(1, ge=1),
    tam_pagina: int = Query(50, ge=1, le=500),
):
    # Valido el filtro de tipo para no devolver cualquier cosa.
    if tipo is not None and tipo not in TIPOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Tipo invalido. Validos: {sorted(TIPOS_VALIDOS)}")

    condiciones, valores = [], []
    if tipo:
        condiciones.append("planet_type = ?")
        valores.append(tipo)
    if mision:
        condiciones.append("mision = ?")
        valores.append(mision)
    where = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

    conn = get_conexion()
    try:
        total = conn.execute(f"SELECT COUNT(*) FROM planets {where}", valores).fetchone()[0]
        salto = (pagina - 1) * tam_pagina
        filas = conn.execute(
            f"SELECT * FROM planets {where} ORDER BY nombre LIMIT ? OFFSET ?",
            valores + [tam_pagina, salto],
        ).fetchall()
    finally:
        conn.close()

    planetas = [Planeta(**dict(f)) for f in filas]
    return PaginaPlanetas(total=total, pagina=pagina, tam_pagina=tam_pagina, planetas=planetas)


@app.get("/planetas/{nombre}", response_model=Planeta)
def obtener_planeta(nombre: str):
    conn = get_conexion()
    try:
        fila = conn.execute("SELECT * FROM planets WHERE nombre = ?", (nombre,)).fetchone()
    finally:
        conn.close()
    if fila is None:
        raise HTTPException(status_code=404, detail=f"No se encontro el planeta '{nombre}'")
    return Planeta(**dict(fila))


@app.get("/estadisticas", response_model=Resumen)
def estadisticas():
    conn = get_conexion()
    try:
        total = conn.execute("SELECT COUNT(*) FROM planets").fetchone()[0]
        if total == 0:
            raise HTTPException(status_code=404, detail="La tabla de planetas esta vacia")
        prom = conn.execute(
            "SELECT AVG(masa_jup), AVG(radio_jup), AVG(periodo_orbital_dias) FROM planets"
        ).fetchone()
        tipos = conn.execute(
            "SELECT planet_type, COUNT(*) FROM planets GROUP BY planet_type ORDER BY COUNT(*) DESC"
        ).fetchall()
    finally:
        conn.close()

    return Resumen(
        total_planetas=total,
        masa_promedio=round(prom[0], 4) if prom[0] is not None else None,
        radio_promedio=round(prom[1], 4) if prom[1] is not None else None,
        periodo_promedio=round(prom[2], 2) if prom[2] is not None else None,
        por_tipo=[ConteoTipo(planet_type=t[0], cantidad=t[1]) for t in tipos],
    )
