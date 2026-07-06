# Integración del trabajo — Evaluacion_Exoplanetas

## Cómo integramos el trabajo en equipo

Durante todo el semestre trabajamos de forma coordinada, principalmente en las sesiones de
taller a través del **AVA (Ambiente Virtual de Aprendizaje) de Duoc UC**, además de
coordinación continua fuera del horario de clases. Cada integrante desarrolló su parte del
proyecto en su propia rama y, una vez que un avance estaba listo y probado, lo integrábamos
a `main` mediante **merge desde la terminal** (`git merge`), después de revisar juntos que
todo funcionara.

Es importante aclarar nuestro flujo real: **la integración se realizó con merge en la
terminal antes de consolidar en `main`**, y no a través de la interfaz formal de Pull
Requests de GitHub. Optamos por este flujo porque trabajábamos de manera sincrónica en las
sesiones del AVA, revisando el código en conjunto en el momento de integrarlo.

## Ramas integradas a `main`

### Rama `api/rest` — Moira Bittner
Desarrollo de la API REST con FastAPI (`api/main.py`, `api/database.py`, `api/models.py`) y
del dashboard Streamlit con las tres vistas (`dashboards/app.py`), junto con los Dockerfiles
de la API y del dashboard. Integrada a `main` mediante merge en terminal tras revisión
conjunta.

### Rama `pipeline_etl` — Nicolás Carrasco
Desarrollo del pipeline ETL (`etl/etl.py`, `etl/clasificar.py`, `etl/Dockerfile.etl`) y del
`docker/docker-compose.yml` que orquesta los servicios. Integrada a `main` mediante merge en
terminal tras revisión conjunta.

## Acuerdo de integración entre ramas

El punto de encuentro entre ambas ramas fue el **esquema de la tabla `planets` en SQLite**.
Lo acordamos al inicio y lo documentamos, de modo que mientras el ETL respetara los nombres
de columna acordados, la API y el dashboard funcionaban sin cambios de código. Este acuerdo
fue lo que nos permitió trabajar en paralelo e integrar con merge sin conflictos mayores.

## Evidencia en el historial

- El commit `Merge branch 'main'` registrado en el historial evidencia la integración de
  trabajo paralelo entre ramas.
- Los commits alternados entre Nicolás Carrasco y Moira Bittner a lo largo de todo el
  historial evidencian la distribución continua del trabajo entre ambos integrantes.
- El detalle completo está en `historial_commits.md` y `ramas.md`.
