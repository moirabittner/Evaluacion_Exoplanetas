# Comparación de Modelos — Proyecto Exoplanetas

## Portafolio de modelos implementados

| Notebook | Modelo | Tipo | Accuracy | F1 Score | ROC-AUC |
|---|---|---|---|---|---|
| 01_regresion_lineal.ipynb | Regresión Lineal | Regresión | R² = 0.017 | — | — |
| 02_arbol_decision.ipynb | Árbol de Decisión | Clasificación | 0.941 | 0.938 | 0.804 |
| 03_logistica_y_clustering.ipynb | Regresión Logística | Clasificación | 0.931 | 0.918 | 0.961 |
| 04_random_forest_gridsearch.ipynb | Random Forest Optimizado | Clasificación | 0.949 | — | 0.992 |

---

## Análisis comparativo

### ¿Qué modelo es el mejor y por qué?

El **Random Forest Optimizado** es el mejor modelo del proyecto. El salto más significativo respecto al Árbol de Decisión baseline es el ROC-AUC: de 0.804 a 0.992. Esto significa que el Random Forest estima probabilidades de pertenencia a cada clase de forma mucho más confiable, especialmente para la clase minoritaria Super-Júpiter hinchado (solo 12 planetas en el dataset).

### Trade-off sesgo / varianza

| Modelo | Sesgo | Varianza | Problema principal |
|---|---|---|---|
| Regresión Lineal | Alto | Bajo | Underfitting: relación masa-radio no es lineal |
| Árbol de Decisión | Bajo | Alto | Riesgo de overfitting con 509 muestras |
| Regresión Logística | Medio | Bajo | Frontera lineal no captura separación curva |
| Random Forest | Bajo | Bajo | Ninguno crítico: ensamble reduce varianza |

### ¿Por qué el R² de la Regresión Lineal es casi nulo?

El R² de 0.017 confirma que la masa no explica el radio de forma lineal. Los gigantes gaseosos saturan en radio (no pueden expandirse indefinidamente aunque la masa aumente), lo que genera una relación curva que una recta no puede capturar. Este resultado justifica el uso de modelos de clasificación basados en densidad (masa/radio³) en lugar de regresión directa.

### ¿Por qué el Árbol tiene mejor Accuracy pero peor ROC-AUC que la Regresión Logística?

El Árbol de Decisión clasifica con reglas de corte duras (si masa > X entonces clase Y), lo que le da un Accuracy alto en los casos donde los grupos están bien separados. Sin embargo, sus probabilidades no están bien calibradas: tiende a asignar probabilidades cercanas a 0 o 1 en lugar de valores intermedios más realistas. La Regresión Logística, en cambio, genera probabilidades suaves mejor calibradas, lo que se refleja en un ROC-AUC superior (0.961 vs 0.804).

### GridSearchCV vs RandomizedSearchCV

| Característica | GridSearchCV | RandomizedSearchCV |
|---|---|---|
| Estrategia | Prueba todas las combinaciones | Muestrea n_iter combinaciones al azar |
| Garantía del óptimo | Sí, dentro del grid definido | No, puede perderse la combinación óptima |
| Velocidad | Más lento (24 combinaciones × 5 folds = 120 fits) | Más rápido (20 combinaciones × 5 folds = 100 fits) |
| Espacio de búsqueda | Limitado a los valores del grid | Puede ser más amplio y continuo |
| Cuándo usarlo | Grid pequeño, tiempo disponible | Grid grande o distribuciones continuas |

Para este proyecto (509 planetas, grid de 24 combinaciones) se usó GridSearchCV como método principal por garantizar el óptimo dentro del espacio definido.

---

## Mejores hiperparámetros encontrados

El GridSearchCV con CV=5 encontró la siguiente combinación óptima para el Random Forest:
- Ver salida de `04_random_forest_gridsearch.ipynb` celda `grid_search.best_params_`

---

## Conclusión

Para clasificar tipos de exoplanetas usando solo masa y radio como features, el **Random Forest Optimizado** es el modelo más fiable y robusto del portafolio. El Árbol de Decisión es la mejor alternativa cuando se requiere interpretabilidad, y la Regresión Logística es la opción más estable cuando se necesitan probabilidades bien calibradas.
