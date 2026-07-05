# Estrategia de Ramas — Evaluacion_Exoplanetas

## Ramas utilizadas

### main
Rama principal de producción. Contiene la versión final integrada del proyecto. Recibe merges desde ramas de desarrollo. El commit #5 del historial (`Merge branch 'main' of https://github.com/moirabittner/Evaluacion1_Exoplanetas`) evidencia la integración de trabajo paralelo entre ramas.

### feature/etl-pipeline
Rama de desarrollo del pipeline ETL (`etl/etl.py`, `etl/clasificar.py`, `etl/requirements.txt`, `etl/Dockerfile.etl`) y el archivo `docker/docker-compose.yml`. Una vez completada, se integró a main mediante merge.

### feature/dashboard
Rama de desarrollo de la API REST con FastAPI (`api/main.py`, `api/database.py`, `api/models.py`) y el dashboard Streamlit con las tres vistas (`dashboards/app.py`). Incluye los Dockerfiles de la API y del dashboard. Se integró a main mediante merge.

### pipeline_etl
Rama alternativa usada durante el desarrollo inicial del ETL.

## Flujo de trabajo

```
feature/etl-pipeline  ──┐
                         ├──► main
feature/dashboard     ──┘
```

## Punto de integración entre ramas

El acuerdo de integración entre ambas ramas fue el esquema de la tabla `planets` en SQLite, documentado en el README y en la guía de integración (`Guia_integracion_Moira_Nicolas.docx`). Mientras el ETL respetara los nombres de columna acordados, la API funcionaba sin cambios de código.

## Convención de mensajes de commit

Los mensajes siguen un formato descriptivo en español que indica qué se hizo en esa sesión de trabajo. Ejemplos del historial real:

- `se agrego modelado supervisado de clasificación de exoplanetas`
- `se terminó el árbol de decisiones y se encontraron problemas con las variables escogidas para la regresión lineal`
- `Se realiza optimización de hiperparámetros`
- `Se realiza fase 3 del proyecto, realizando creación de columnas nuevas, aplicando feauting engineering, escalamiento, codificación y pipeline`
- `eliminar duplicados y columnas con >80% nulos (a revisión)`
