# Evaluación Semestral — Exoplanetas

Proyecto integrador del ramo **SCY1101 — Programación para la Ciencia de Datos** (Duoc UC).
A lo largo del semestre tomamos un mismo dataset de exoplanetas de la NASA y lo trabajamos
en tres etapas, desde la limpieza de los datos hasta una solución completa de extremo a
extremo desplegada con Docker.

## Integrantes

- **Moira Bittner**
- **Nicolás Carrasco**

Grupo 6 · Sección 001D

## Origen y descripción de los datos

Los datos provienen de [Google Dataset Search](https://datasetsearch.research.google.com/):
un dataset público de la NASA con información de **exoplanetas confirmados**. Incluye
variables como período orbital, semieje mayor, excentricidad, masa y radio del planeta,
temperatura y radio de la estrella anfitriona, entre otras.

A partir de estas variables construimos la variable derivada `planet_type`, que clasifica
cada planeta según sus características físicas y es el foco predictivo de todo el proyecto.

---

## Las tres partes del semestre

El proyecto se desarrolló de forma incremental: cada evaluación reutiliza y amplía el
trabajo de la anterior.

### Evaluación 1 — Limpieza y Feature Engineering
`Evaluacion1_Exoplanetas.ipynb`

Punto de partida del proyecto. Aquí preparamos el dataset para poder analizarlo:

- Eliminación de columnas con más del 80% de valores nulos.
- Corrección de outliers con *capping* por rango intercuartílico (IQR).
- Imputación de valores faltantes con la mediana.
- Creación de variables derivadas clave, como `pl_density` (masa / radio³) y `planet_type`.
- Normalización con `MinMaxScaler` y codificación con `LabelEncoder`.

**Salida:** el dataset limpio `planets_clean.csv`, base para las etapas siguientes.

### Evaluación 2 — Modelos predictivos y clustering
`Evaluacion2_Exoplanetas.ipynb`

Usamos los datos para responder la pregunta: *¿podemos predecir el tipo de planeta usando
solo su masa y su radio?* El trabajo se divide en tres partes:

- **Modelos supervisados:** Regresión Lineal (diagnóstico masa→radio), Árbol de Decisión
  (Accuracy ≈ 94%) y Regresión Logística (ROC-AUC ≈ 0.96).
- **Clustering:** `KMeans` con `K=3`, validado con el método del codo, Silhouette Score y PCA.
- **Optimización:** Random Forest ajustado con `GridSearchCV` y `RandomizedSearchCV`
  (mejor modelo: Accuracy ≈ 95%, ROC-AUC ≈ 0.99).

Los notebooks de cada modelo, junto con su comparación y justificación técnica, también
están organizados en la carpeta `Evaluacion3_Exoplanetas/models/`.

### Evaluación 3 / Evaluación Final Transversal — Solución end-to-end
`Evaluacion3_Exoplanetas/`

Convertimos el análisis en un sistema profesional completo que integra **tres fuentes de
datos** y se despliega con Docker:

- **Pipeline ETL** (`etl/`) que integra el CSV, la API REST de la NASA (servicio TAP) y una
  base de datos **SQLite**, con validación de esquemas y manejo de errores.
- **API REST** con FastAPI (`api/`): endpoints `/planetas`, `/estadisticas` y `/salud`.
- **Dashboard interactivo** con Streamlit (`dashboards/`): tres vistas diferenciadas por
  audiencia (Ejecutiva, Técnica y Operativa).
- **Containerización** con Docker y `docker-compose` (`docker/`).
- **Testing automatizado** (`tests/`) y **CI/CD** con GitHub Actions (`.github/workflows/`).

Ver el detalle completo en `Evaluacion3_Exoplanetas/README.md`.

---

## Estructura del repositorio

```
Evaluacion_Exoplanetas/
├── Evaluacion1_Exoplanetas.ipynb    # Evaluación 1: limpieza y feature engineering
├── Evaluacion2_Exoplanetas.ipynb    # Evaluación 2: modelos y clustering
├── Evaluacion3_Exoplanetas/         # Evaluación 3 / EFT: solución end-to-end
│   ├── etl/  api/  dashboards/  docker/  models/  tests/  docs/  scripts/  data/
│   └── README.md
├── Datos/
│   ├── planets.csv                  # Dataset original (NASA)
│   └── planets_clean.csv            # Dataset limpio (salida de Eval 1)
├── repo/                            # Evidencias de colaboración en Git (todo el semestre)
├── .github/workflows/ci.yml        # Workflow de CI/CD (GitHub Actions)
└── README.md                       # Este archivo
```

## Justificación del entorno

Trabajamos con **Jupyter Notebook en local** (Eval 1 y 2) y con **VS Code + terminal**
(Eval 3), principalmente porque la integración con GitHub es más directa: desde la terminal
hacemos `git add`, `commit`, `push`, `pull` y `merge` sin pasos extra. Además, trabajar en
local nos da acceso directo a los archivos del proyecto (`planets.csv`, `planets_clean.csv`)
y no dependemos de conexión a internet para ejecutar los notebooks.

## Cómo ejecutar cada parte

**Evaluación 1 y 2 (notebooks):**

```bash
pip install "pandas>=2.0" "numpy>=1.24" "scikit-learn>=1.3" "matplotlib>=3.7" "seaborn>=0.12" jupyter
jupyter notebook Evaluacion1_Exoplanetas.ipynb   # o Evaluacion2_Exoplanetas.ipynb
```

Ejecutar de la primera a la última celda con `Run All`. Todos los `random_state` están
fijos, así que los resultados son reproducibles.

**Evaluación 3 (sistema completo con Docker):**

```bash
cd Evaluacion3_Exoplanetas/docker
docker-compose up --build
```

Luego abrir el dashboard en `localhost:8501` y la documentación de la API en
`localhost:8000/docs`. Ver la guía detallada en `Evaluacion3_Exoplanetas/README.md`.

## Reproducibilidad

- Los datasets (`planets.csv`, `planets_clean.csv`) están congelados en el repositorio; no se
  descargan en tiempo de ejecución.
- Los modelos usan `random_state` fijo (42 o 99 según la celda).
- El sistema end-to-end se levanta de forma reproducible con un solo comando gracias a Docker.
