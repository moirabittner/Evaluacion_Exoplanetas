# Problemas técnicos y decisiones — Evaluacion_Exoplanetas

## Cómo gestionamos los problemas

Los problemas técnicos que fueron surgiendo los discutimos y resolvimos **en conjunto
durante las sesiones de taller a través del AVA de Duoc UC**, en lugar de usar la pestaña
formal de *Issues* de GitHub. A continuación documentamos los principales problemas que
enfrentamos y cómo los resolvimos, como evidencia del trabajo colaborativo y de la toma de
decisiones técnicas a lo largo del semestre.

### Problema 1 — Variables `pl_bmassj` y `pl_orbeccen` constantes tras la imputación
- **Situación:** al imputar con mediana en la Evaluación 1, estas columnas quedaron con
  desviación estándar casi cero, lo que las inutilizaba para los modelos.
- **Decisión:** volver al CSV original (`planets.csv`) para los modelos de la Evaluación 2 y
  trabajar solo con los 509 planetas que tienen masa y radio observados de verdad.
- **Estado:** Resuelto ✅

### Problema 2 — Gráficos de regresión lineal con datos apilados en x≈1.0
- **Situación:** al usar `pl_bmassj_norm` para graficar, los puntos quedaban comprimidos por
  la normalización MinMax sobre datos con outliers extremos.
- **Decisión:** usar las variables originales `st_teff` y `st_rad`, con distribución natural
  adecuada para graficar.
- **Estado:** Resuelto ✅

### Problema 3 — Integración del ETL con el esquema de la API
- **Situación:** había que acordar los nombres exactos de las columnas de la tabla `planets`
  para que el ETL (Nicolás) y la API (Moira) fueran compatibles sin tocar el código del otro.
- **Decisión:** acordamos y documentamos el esquema de la tabla; el ETL se adaptó para
  respetar esos nombres.
- **Estado:** Resuelto ✅

### Problema 4 — `NaN` en la columna `planet_type` al entrenar modelos
- **Situación:** `planet_type` tenía valores NaN en algunas filas, lo que causaba error al
  pasarla como target a los modelos de clasificación.
- **Decisión:** agregar `dropna(subset=['planet_type'])` antes de separar features y target.
- **Estado:** Resuelto ✅

### Problema 5 — Falta de evidencia de CI/CD
- **Situación:** la EFT requiere evidencia de automatización y CI/CD.
- **Decisión:** crear `.github/workflows/ci.yml` con GitHub Actions, que instala las
  dependencias del ETL y la API y ejecuta `pytest tests/` automáticamente en cada push.
- **Estado:** Resuelto ✅
