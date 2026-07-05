# /models/ — Portafolio de Modelos Machine Learning

Carpeta con los modelos predictivos implementados en la Evaluación 2 del proyecto de exoplanetas.

## Notebooks disponibles

| Archivo | Modelo | Tipo |
|---|---|---|
| `01_regresion_lineal.ipynb` | Regresión Lineal | Regresión |
| `02_arbol_decision.ipynb` | Árbol de Decisión | Clasificación |
| `03_logistica_y_clustering.ipynb` | Regresión Logística + KMeans | Clasificación + Clustering |
| `04_random_forest_gridsearch.ipynb` | Random Forest con GridSearchCV y RandomizedSearchCV | Clasificación optimizada |
| `comparacion_modelos.md` | Tabla comparativa y análisis de todos los modelos | Documentación |

## Cómo ejecutar

1. Asegurarse de tener el dataset en `../Datos/planets.csv`
2. Instalar dependencias:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```
3. Ejecutar los notebooks en orden (01 → 02 → 03 → 04), ya que cada uno reutiliza `df_work` generado en la celda de preparación de datos.

## Dataset utilizado

Se usa `planets.csv` (dataset original sin imputar) y no `planets_clean.csv`, porque la imputación con mediana dejó la columna `pl_bmassj` constante, lo que destruía la variabilidad real de los datos. Se trabaja con los 509 planetas que tienen masa y radio observados de forma real.

## Variable objetivo

`planet_type` se calcula a partir de la densidad (masa / radio³):
- **Rocoso/Compacto**: densidad > 0.3
- **Neptuno-like**: 0.1 < densidad ≤ 0.3
- **Super-Júpiter hinchado**: densidad ≤ 0.1
