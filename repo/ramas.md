# Estrategia de Ramas — Evaluacion_Exoplanetas

## Ramas utilizadas

### `main`
Rama principal de producción. Contiene la versión final integrada del proyecto. Recibe los
avances desde las ramas de desarrollo mediante **merge en terminal**. El commit
`Merge branch 'main'` del historial evidencia la integración de trabajo paralelo.

### `pipeline_etl` — Nicolás Carrasco
Rama de desarrollo del pipeline ETL (`etl/etl.py`, `etl/clasificar.py`,
`etl/requirements.txt`, `etl/Dockerfile.etl`) y del archivo `docker/docker-compose.yml`.
Una vez completada, se integró a `main` mediante merge desde la terminal.

### `api/rest` — Moira Bittner
Rama de desarrollo de la API REST con FastAPI (`api/main.py`, `api/database.py`,
`api/models.py`) y del dashboard Streamlit con las tres vistas (`dashboards/app.py`),
incluyendo los Dockerfiles de la API y del dashboard. Se integró a `main` mediante merge
desde la terminal.

## Flujo de trabajo

```
pipeline_etl  ──┐
                 ├──►  main   (merge en terminal, tras revisión conjunta)
api/rest      ──┘
```

## Punto de integración entre ramas

El acuerdo de integración entre ambas ramas fue el **esquema de la tabla `planets` en
SQLite**. Mientras el ETL respetara los nombres de columna acordados, la API y el dashboard
funcionaban sin cambios de código. Ese acuerdo nos permitió desarrollar en paralelo e
integrar con merge sin conflictos mayores.

## Cómo trabajamos

Nos coordinamos principalmente en las sesiones de taller a través del **AVA de Duoc UC**.
Cada integrante desarrollaba en su rama y, al integrar, hacíamos `git merge` desde la
terminal revisando juntos que el código funcionara antes de consolidar en `main`.

## Convención de mensajes de commit

Los mensajes siguen un formato descriptivo en español que indica qué se hizo en cada sesión.
Ejemplos del historial real:

- `se agrego modelado supervisado de clasificación de exoplanetas`
- `se terminó el árbol de decisiones y se encontraron problemas con las variables escogidas`
- `Se realiza optimización de hiperparámetros`
- `Corrige ETL (NASA, ruta CSV, validación de esquemas) y Docker; agrega tests`
- `Agrega workflow de CI/CD con GitHub Actions`
