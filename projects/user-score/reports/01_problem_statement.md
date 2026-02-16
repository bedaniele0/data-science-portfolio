# Problem Statement - Prediccion de User Score

**Autor**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428
**Fecha**: 19/01/2026
**Versión**: 1.0

---

## 1. Contexto de Negocio

### Situacion Actual
La organizacion cuenta con un dataset historico de videojuegos (metacritic-like) y no existe un analisis sistematico de los factores que explican el `user_score`. Esto limita la capacidad de priorizar mejoras de producto o contenido basadas en percepcion del usuario.

### Problematica
No hay un modelo que estime el `user_score` esperado ni un analisis claro de variables que influyen en la percepcion de los usuarios.

---

## 2. Problema a Resolver

### Definicion Clara (2-3 oraciones)
Predecir el `user_score` de un videojuego a partir de variables disponibles en el dataset (por ejemplo `meta_score`, plataforma, fecha, desarrollador y generos). El objetivo es obtener un modelo de regresion baseline que permita estimar la percepcion del usuario y derivar insights accionables.

### Alcance
**En Scope:**
- ✅ EDA completo del dataset
- ✅ Limpieza y transformaciones basicas
- ✅ Modelado baseline y una mejora
- ✅ Reporte de resultados e insights

**Out of Scope:**
- ❌ Despliegue en produccion
- ❌ MLOps y monitoreo operativo real
- ❌ Dashboards avanzados

---

## 3. Objetivos Especificos

### Objetivo de Negocio
Anticipar la percepcion del usuario (`user_score`) e identificar factores que influyen en la evaluacion para soportar decisiones de mejora de producto/contenido.

### Objetivo Tecnico
Construir un modelo de regresion con **MAE ≤ 0.60** y **R2 ≥ 0.50** en validacion.

---

## 4. Metricas de Exito

### Metricas de Negocio
| Metrica | Baseline Actual | Objetivo | Medicion |
|---------|-----------------|----------|----------|
| Capacidad de anticipar percepcion | No existe | Insights claros | Por reporte |
| Identificacion de drivers | No existe | Top 5 drivers | Por analisis |

### Metricas Tecnicas
| Metrica | Baseline | Objetivo | Criticidad |
|---------|----------|----------|------------|
| MAE | N/A | ≤ 0.60 | Alta |
| R2 | N/A | ≥ 0.50 | Alta |
| RMSE | N/A | Minimizar | Media |

### Criterio de Exito
El proyecto es exitoso si se logra un modelo con MAE ≤ 0.60 y R2 ≥ 0.50, junto con insights accionables sobre variables influyentes.

---

## 5. Stakeholders

### Sponsor del Proyecto
- **Nombre**: N/A (proyecto personal/portafolio)
- **Rol**: N/A
- **Responsabilidad**: N/A

### Usuarios Finales
- **Equipo**: Analista/DS (portafolio)
- **Uso**: Analisis y presentacion de hallazgos
- **Expectativas**: Insights claros y modelo baseline

### Equipo Tecnico
| Rol | Nombre | Responsabilidad |
|-----|--------|-----------------|
| Data Scientist | Ing. Daniel Varela Perez | EDA, modelado, evaluacion |

### Matriz RACI
| Actividad | Data Scientist |
|-----------|----------------|
| Definir problema | R/A |
| EDA | R/A |
| Feature Engineering | R/A |
| Modelado | R/A |
| Validacion | R/A |
| Cierre | R/A |

---

## 6. Datos Disponibles

### Dataset A/B/C (DVP-PRO)

- **Dataset A (raw)**: `data/data.csv`
- **Dataset B (prod/input)**: `data/prod/input.csv`
- **Dataset C (prod/actuals)**: `data/prod/actuals.csv`

### Fuentes de Datos
| Fuente | Descripcion | Actualizacion | Acceso |
|--------|-------------|---------------|--------|
| data.csv | Dataset historico de videojuegos | Estatica | ✅ Disponible |

### Datos Requeridos vs Disponibles
- **Requeridos**: user_score, meta_score, platform, date, developers, genres, esrb_rating
- **Disponibles**: Todos los campos requeridos en `data.csv`
- **Gap**: No se requieren fuentes externas

---

## 7. Valor Esperado (ROI)

### Analisis Costo-Beneficio (estimado)
**Beneficios esperados:**
- Generar un caso de portafolio con modelo funcional y hallazgos accionables.
- Ahorro de tiempo analitico futuro mediante pipeline reproducible.

**Costos estimados:**
- 3-4 dias de trabajo individual.

**ROI:**
- ROI cualitativo alto (portafolio + capacidad analitica demostrada).

### Riesgos Economicos
| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| Dataset con señal limitada | Media | Media | Probar modelos baseline y features derivadas |
| Objetivos tecnicos no alcanzados | Media | Media | Ajuste de features y validacion |

---

## 8. Restricciones y Supuestos

### Restricciones
- **Tiempo**: 3-4 dias
- **Recursos**: 1 persona
- **Tecnicas**: Sin despliegue ni MLOps

### Supuestos
- ✅ El `user_score` tiene suficiente variabilidad para modelado
- ✅ `meta_score` aporta señal explicativa

---

## 9. Timeline y Fases (S-Lite)

| Fase | Duracion | Entregables | Responsable |
|------|----------|-------------|-------------|
| F0 - Contexto | 0.5 dias | Problem statement, KPI, business case | DS |
| F3 - EDA | 1-1.5 dias | EDA report + data quality | DS |
| F5 - Modelado | 1 dia | Baseline + mejora | DS |
| F6 - Validacion | 0.5 dias | Model evaluation | DS |
| F9 - Cierre | 0.5 dias | Final report + ROI | DS |

---

## 10. Decisiones que se Tomaran
1. Priorizar generos/plataformas con mejor percepcion de usuarios.
2. Identificar combinaciones de variables que tienden a mayor `user_score`.
3. Decidir si el dataset es suficiente para un modelo mas avanzado.

### Criterios de Go/No-Go
**Go (continuar a mejora adicional):**
- MAE ≤ 0.60 y R2 ≥ 0.50

**No-Go:**
- R2 < 0.30 y sin variables con señal clara

---

## 11. Criterios de Aceptacion

### Tecnicos
- [ ] MAE ≤ 0.60
- [ ] R2 ≥ 0.50
- [ ] Validacion reproducible

### Negocio
- [ ] Insights accionables documentados

---

## 12. Proximos Pasos
1. Ejecutar EDA (F3)
2. Construir baseline y mejora (F5)
3. Evaluar y cerrar (F6/F9)

---

## 13. Aprobaciones

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Data Science Lead | Ing. Daniel Varela Perez | __________ | 19/01/2026 |

---

## 14. Control de Cambios

| Version | Fecha | Cambio | Autor |
|---------|-------|--------|-------|
| 1.0 | 19/01/2026 | Version inicial | Ing. Daniel Varela Perez |

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
