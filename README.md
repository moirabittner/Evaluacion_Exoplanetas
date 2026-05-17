# Evaluación 1 — Exoplanetas

Primera evaluación del ramo Programación de Ciencia de Datos.

## Integrantes

- Moira Bittner
- Nicolás Carrasco

## Origen y descripción de los datos

Los datos que usamos los encontramos en [Google Dataset Search](https://datasetsearch.research.google.com/). Es un dataset público de la NASA con información de exoplanetas confirmados. Incluye datos como el período orbital, semieje mayor, excentricidad, masa, radio del planeta, temperatura de la estrella, entre otros.

## Justificación del entorno

Decidimos trabajar con **Jupyter Notebook en local** principalmente porque sentimos que la integración con GitHub es mucho más directa. Desde la terminal podemos hacer `git add`, `commit`, `push` y `pull` sin complicaciones, cosa que en Google Colab requiere pasos extra.

Además, al trabajar en local tenemos acceso directo a los archivos del proyecto (como `planets.csv` y `planets_clean.csv`), sin tener que andar montando extensiones. También nos ahorramos depender de internet para poder ejecutar el notebook.

# Evaluación 2 — Modelos predictivos sobre exoplanetas

Segunda evaluación del ramo Programación para la Ciencia de Datos. En esta parte tomamos el mismo dataset de la NASA y lo usamos para entrenar y comparar modelos de Machine Learning, hacer clustering y optimizar hiperparámetros.

## Pregunta de investigación

¿Podemos predecir el **tipo de planeta** (rocoso, neptuno-like o super-Júpiter hinchado) usando solamente su **masa** y su **radio**?

Para responderla, creamos la variable derivada `planet_type` a partir de la densidad (`masa / radio³`) cortada en tres bandas físicamente reconocidas, y nos quedamos con los **509 planetas** del dataset original que tienen masa y radio observados de verdad (no imputados).

## Etapas del trabajo

La Evaluación 2 está organizada en tres partes dentro del mismo notebook:

- **Parte 1 — Modelos supervisados.** Entrenamos tres modelos con parámetros por defecto:
  - *Regresión Lineal* (masa → radio): R² ≈ 0.017 → confirma que la relación no es lineal.
  - *Árbol de Decisión*: Accuracy ≈ 94.1%, ROC-AUC ≈ 0.80.
  - *Regresión Logística*: Accuracy ≈ 93.1%, ROC-AUC ≈ 0.96.
- **Parte 2 — Clustering.** Aplicamos `KMeans` con `K=3`, validado con método del codo, Silhouette Score (≈ 0.82) y PCA. El producto final es un mapa estratégico con las zonas físicas sombreadas.
- **Parte 3 — Optimización.** Re-entrenamos un Árbol como baseline y lo comparamos contra un **Random Forest optimizado con `GridSearchCV`** (probamos `cv=5` y `cv=10`). El mejor modelo final alcanza Accuracy ≈ 95.1% y ROC-AUC ≈ 0.994.

## Algoritmos utilizados

| Algoritmo | Tipo | Rol en el análisis |
|---|---|---|
| Regresión Lineal | Regresión | Diagnóstico de la relación masa-radio |
| Árbol de Decisión | Clasificación | Modelo interpretable de referencia |
| Regresión Logística | Clasificación | Comparación lineal multiclase |
| KMeans | Clustering | Validación no supervisada de la estructura |
| Random Forest + GridSearchCV | Clasificación | Modelo final optimizado |

## Conclusión

El **Random Forest optimizado** es el mejor modelo del proyecto. La ganancia más relevante respecto del árbol único no está en el Accuracy global, sino en el ROC-AUC: pasamos de 0.91 a 0.994, lo que significa probabilidades mucho más confiables para las clases minoritarias (Neptuno-like y Super-Júpiter hinchado).

# Guía de uso del proyecto

## Estructura de carpetas

```
Evaluacion1_Exoplanetas/
├── Evaluacion1_Exoplanetas.ipynb   # Notebook principal (Eval 1 + Eval 2)
├── Datos/
│   ├── planets.csv                  # Dataset original (NASA)
│   └── planets_clean.csv            # Dataset limpio (salida de Eval 1)
└── README.md                        # Este archivo
```

## Requisitos

- **Python 3.10** o superior.
- **Jupyter Notebook** o JupyterLab (también funciona en VS Code con la extensión de Jupyter).
- **Git** para clonar el repositorio (opcional).

## Instalación paso a paso

1. **Clonar el repositorio** (o descargar la carpeta como zip):

   ```bash
   git clone <url-del-repositorio>
   cd Evaluacion2Final/Evaluacion1_Exoplanetas
   ```

2. **Crear un entorno virtual** (recomendado, pero opcional):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate     # en macOS / Linux
   .venv\Scripts\activate        # en Windows
   ```

3. **Instalar las dependencias**:

   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn jupyter
   ```

4. **Abrir el notebook**:

   ```bash
   jupyter notebook Evaluacion1_Exoplanetas.ipynb
   ```

   o, si prefieres VS Code:

   ```bash
   code Evaluacion1_Exoplanetas.ipynb
   ```

5. **Ejecutar el notebook** desde la primera celda hasta la última con `Run All` (o `Shift + Enter` celda por celda). Las celdas están ordenadas de forma secuencial: limpieza de datos → feature engineering → modelos supervisados → clustering → optimización.

## Dependencias

Todas las dependencias son de uso libre y se pueden instalar con `pip`. Versiones probadas:

| Paquete | Versión mínima | Uso en el proyecto |
|---|---|---|
| `python` | 3.10 | Lenguaje base |
| `pandas` | 2.0 | Carga y manipulación del CSV |
| `numpy` | 1.24 | Operaciones numéricas y arrays |
| `scikit-learn` | 1.3 | Modelos (`LinearRegression`, `DecisionTreeClassifier`, `LogisticRegression`, `RandomForestClassifier`, `KMeans`), `train_test_split`, `GridSearchCV`, métricas y `MinMaxScaler` |
| `matplotlib` | 3.7 | Gráficos base (scatter, barras, curvas) |
| `seaborn` | 0.12 | Heatmaps de matrices de confusión y scatterplots |
| `jupyter` | 7.0 | Ejecución del notebook |

Para instalar todo en una sola línea:

```bash
pip install "pandas>=2.0" "numpy>=1.24" "scikit-learn>=1.3" "matplotlib>=3.7" "seaborn>=0.12" jupyter
```

## Reproducibilidad

- Todos los `train_test_split` y modelos del notebook usan `random_state` fijo (42 o 99 según la celda), así que los resultados son **reproducibles** entre corridas.
- El archivo `planets.csv` está congelado dentro del repositorio; **no se descarga en tiempo de ejecución**, por lo que el notebook funciona sin conexión a internet.

## Problemas comunes

- **`ModuleNotFoundError: No module named 'sklearn'`** → falta instalar `scikit-learn` (`pip install scikit-learn`).
- **Gráficos que no se muestran** → en VS Code asegúrate de tener seleccionado el kernel del entorno virtual donde instalaste los paquetes.
- **Resultados ligeramente distintos a los del informe** → revisa que estés cargando `planets.csv` (no `planets_clean.csv`) en la parte de Evaluación 2 y que el `random_state` esté en el valor indicado en cada celda.
