# Parte de Moira - API, Dashboard y Docker

Esta es mi parte (Moira) de la Evaluacion 3 de Exoplanetas. Yo hice la API,
el dashboard y los Dockerfiles. Nicolas hace el ETL, la base de datos
definitiva, el docker-compose general y la documentacion tecnica.

## Carpetas

- `api/` - API hecha con FastAPI que lee los datos desde SQLite.
- `dashboards/` - dashboard en Streamlit con tres vistas.
- `docker/` - los Dockerfiles de la API y del dashboard.
- `scripts/` - `crear_bd.py`, que arma una base de prueba desde el CSV.
- `tests/` - pruebas de la API.
- `data/` - el CSV y la base `exoplanets.db`.

## La base de datos

Tabla **`planets`** (este es el acuerdo con Nicolas: su ETL escribe esta
misma tabla con estas columnas):

nombre, estrella, metodo_descubrimiento, mision, planetas_en_sistema,
periodo_orbital_dias, semieje_mayor_au, excentricidad, masa_jup, radio_jup,
densidad, distancia_pc, temp_estrella_k, masa_estrella, radio_estrella y
**planet_type** (la clasificacion).

La clasificacion `planet_type` la calculo segun el radio: menor a 0.16 es
Rocoso, menor a 0.28 es Neptuniano y el resto Gigante Gaseoso.

## Endpoints de la API

- `GET /salud` - dice si la base conecta.
- `GET /planetas` - lista de planetas, con filtros `?tipo=` y `?mision=` y paginas (`?pagina=`, `?tam_pagina=`).
- `GET /planetas/{nombre}` - un planeta puntual.
- `GET /estadisticas` - totales, promedios y conteo por tipo.
- `GET /docs` - documentacion que genera FastAPI sola.

## Como correr

```
# 1. Crear la base de prueba
pip install -r scripts/requirements.txt
python scripts/crear_bd.py

# 2. Levantar la API
pip install -r api/requirements.txt
uvicorn api.main:app --reload        # http://localhost:8000/docs

# 3. Levantar el dashboard (en otra terminal)
pip install -r dashboards/requirements.txt
streamlit run dashboards/app.py      # http://localhost:8501

# Pruebas
pytest tests/
```

## Las tres vistas del dashboard

- **Ejecutiva**: numeros generales y los planetas por tipo.
- **Tecnica**: graficos de masa/radio y los resultados de los modelos de la Evaluacion 2.
- **Operativa**: tabla con filtro y buscador por planeta.
