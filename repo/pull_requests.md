# Pull Requests — Evaluacion_Exoplanetas

## Pull Requests realizados

### PR #1 — Integración del pipeline ETL con la base de datos
- **Rama origen:** feature/etl-pipeline
- **Rama destino:** main
- **Descripción:** Implementación completa del pipeline ETL (`etl.py`, `clasificar.py`) con las tres fuentes de datos (CSV, API NASA, SQLite), validación de esquemas, manejo de errores y Dockerfile del ETL.
- **Revisora:** moibittner
- **Estado:** Mergeado ✅

### PR #2 — API REST y Dashboard Streamlit
- **Rama origen:** feature/dashboard
- **Rama destino:** main
- **Descripción:** Implementación de la API REST con FastAPI (endpoints `/planetas`, `/estadisticas`, `/salud`, `/docs`) y el dashboard Streamlit con tres vistas diferenciadas por audiencia: Ejecutiva, Técnica y Operativa. Incluye `Dockerfile.api` y `Dockerfile.dashboard`.
- **Revisor:** Nicolas Carrasco
- **Estado:** Mergeado ✅

### PR #3 — Orquestación Docker completa
- **Rama origen:** feature/etl-pipeline
- **Rama destino:** main
- **Descripción:** Archivo `docker-compose.yml` que orquesta los tres servicios (etl, api, dashboard) con el volumen compartido `db-data` y las variables de entorno `DB_PATH` y `API_URL`. El servicio `api` depende de `etl` y `dashboard` depende de `api`.
- **Revisora:** moibittner
- **Estado:** Mergeado ✅

## Evidencia de trabajo colaborativo en el historial

El commit `Merge branch 'main' of https://github.com/moirabittner/Evaluacion1_Exoplanetas` registrado en el historial confirma que se trabajó con ramas paralelas y se integraron mediante merge. Los commits alternados entre Nicolas Carrasco y moibittner a lo largo de todo el historial evidencian la distribución continua del trabajo entre ambos integrantes.
