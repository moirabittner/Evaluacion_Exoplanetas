# Issues — Evaluacion_Exoplanetas

## Issues registrados durante el desarrollo

### Issue #1 — Variables pl_bmassj y pl_orbeccen constantes tras normalización
- **Título:** Variables pl_bmassj y pl_orbeccen quedan constantes tras imputación con mediana
- **Descripción:** Al aplicar imputación con mediana en la Evaluación 1, las columnas `pl_bmassj` y `pl_orbeccen` quedaron con desviación estándar prácticamente cero, lo que inutilizaba estas variables para los modelos.
- **Decisión tomada:** Volver al CSV original (`planets.csv`) para los modelos de la Evaluación 2 y trabajar solo con los 509 planetas que tienen masa y radio observados de verdad. Documentado en el commit: `se terminó el árbol de decisiones y se encontraron problemas con las variables escogidas para la regresión lineal`.
- **Estado:** Cerrado ✅

### Issue #2 — Gráficos de regresión lineal con datos apilados en x≈1.0
- **Título:** Scatter de masa vs radio muestra todos los puntos apilados por escala
- **Descripción:** Al usar `pl_bmassj_norm` para graficar, todos los valores quedaban comprimidos en x≈1.0 por la normalización MinMax sobre datos con outliers extremos.
- **Decisión tomada:** Cambiar a las variables originales `st_teff` y `st_rad` (temperatura y radio estelar) que tienen distribución natural adecuada para graficar.
- **Estado:** Cerrado ✅

### Issue #3 — Integración ETL con esquema de la API
- **Título:** Definir esquema exacto de la tabla planets para compatibilidad ETL-API
- **Descripción:** Necesidad de acordar los nombres exactos de las 16 columnas de la tabla `planets` en SQLite para que el ETL (Nicolas) y la API (Moira) fueran compatibles sin modificar el código de cada uno.
- **Decisión tomada:** Moira redactó la guía de integración (`Guia_integracion_Moira_Nicolas.docx`) con el esquema exacto. Nicolas adaptó el ETL para respetar esos nombres.
- **Estado:** Cerrado ✅

### Issue #4 — NaN en columna planet_type al entrenar modelos
- **Título:** ValueError: Input contains NaN al entrenar modelos de clasificación
- **Descripción:** La columna `planet_type` tenía valores NaN en algunas filas, lo que causaba error al pasarla como target a `LogisticRegression`.
- **Decisión tomada:** Agregar `dropna(subset=['planet_type'])` antes de separar features y target. Documentado en el proceso de corrección de la Evaluación 2.
- **Estado:** Cerrado ✅

### Issue #5 — CI/CD: workflow de GitHub Actions para tests automáticos
- **Título:** Implementar CI Pipeline con GitHub Actions
- **Descripción:** La EFT requiere evidencia de CI/CD. Se necesitaba un workflow que ejecutara automáticamente los tests unitarios en cada push a main o develop.
- **Decisión tomada:** Crear `.github/workflows/ci.yml` que instala dependencias del ETL y la API y ejecuta `pytest tests/ -v`.
- **Estado:** Cerrado ✅
