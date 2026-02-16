# Problem Statement - Walmart Demand Forecasting & Inventory Optimization

**Autor**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428
**Fecha**: 4 de Diciembre, 2024
**Versión**: 1.0
**Proyecto**: Walmart Demand Forecasting & Inventory Optimization

---

## 📋 FASE 0: DEFINICIÓN DEL PROBLEMA (DVP-PRO)

---

## 1. Contexto de Negocio

### Situación Actual

Walmart, la cadena de retail más grande del mundo, opera miles de tiendas que gestionan millones de transacciones diarias. En este proyecto, nos enfocamos en **10 tiendas ubicadas en 3 estados de Estados Unidos** (California, Texas, Wisconsin) que manejan un inventario de **3,049 productos únicos** distribuidos en 3 categorías principales:

- **HOBBIES**: Artículos de entretenimiento, deportes, juguetes
- **FOODS**: Productos alimenticios y bebidas
- **HOUSEHOLD**: Artículos para el hogar y cuidado personal

### Problemática Identificada

El retail moderno enfrenta dos desafíos críticos simultáneos:

1. **Stockouts (Quiebres de Inventario)**:
   - Pérdida de ventas cuando productos no están disponibles
   - Insatisfacción del cliente y pérdida de lealtad
   - Oportunidad perdida de ingresos
   - Impacto: **4-8% de pérdida de ventas** en promedio en retail

2. **Exceso de Inventario**:
   - Costos de almacenamiento elevados
   - Riesgo de obsolescencia (especialmente productos perecederos)
   - Capital inmovilizado
   - Mermas por vencimiento
   - Impacto: **20-30% del valor del inventario** en costos asociados

### Madurez Analítica Actual

**Estado Baseline**: Métodos tradicionales de forecasting:
- Promedios móviles simples
- Forecasting manual basado en experiencia
- Reposición reactiva (cuando el inventario baja de umbral)
- **Precisión estimada**: 60-70% (MAE alto, frecuentes errores)

**Oportunidad**: Implementar forecasting avanzado con Machine Learning y optimización de inventario.

### Estado actual del proyecto (demo/portafolio)

Este repositorio presenta una **demo técnica** basada en el dataset público M5, con foco en reproducibilidad y comunicación de resultados:

- Modelo LightGBM preentrenado con pipeline de features (lags, calendario, precios, eventos, SNAP).
- API FastAPI y dashboard Streamlit operativos en local.
- Predicciones sobre un subconjunto de datos y ejemplos controlados.
- Tracking opcional en MLflow local.

**Fuera de la demo** (planteado a nivel diseño):
- Integración con ERP/WMS y flujos de reposición reales.
- Optimización de inventario en vivo (EOQ, puntos de reorden).
- Retraining automatizado diario y despliegue productivo.

---

## 2. Problema a Resolver

### Definición del Problema

**Desarrollar un sistema inteligente de predicción de demanda y optimización de inventario que permita:**

1. **Predecir con alta precisión** las ventas diarias de cada producto en cada tienda para los próximos **28 días**
2. **Optimizar los niveles de inventario** basándose en las predicciones para minimizar stockouts y costos de almacenamiento
3. **Identificar patrones de demanda** (estacionalidad, eventos especiales, efectos precio)
4. **Generar recomendaciones accionables** para managers de tienda y planificadores de inventario

### Alcance del Proyecto

**Incluye (demo actual):**
- ✅ Forecasting de demanda a nivel producto‑tienda (dataset M5)
- ✅ Horizonte de predicción: 28 días
- ✅ Variables externas: precios, eventos y SNAP
- ✅ API REST para predicciones bajo demanda
- ✅ Dashboard interactivo para visualización
- ✅ Documentación técnica y de negocio

**Planificado (fuera de demo):**
- ⏳ Forecasting jerárquico con reconciliación multi‑nivel
- ⏳ Optimización de inventario basada en forecast (EOQ/puntos de reorden)
- ⏳ Retraining automatizado y despliegue productivo

**No incluye:**
- ❌ Forecasting en tiempo real (scope: batch diario)
- ❌ Recomendaciones de pricing dinámico
- ❌ Integración con sistemas ERP existentes
- ❌ Forecasting de productos nuevos (cold start)
- ❌ Cobertura de SKUs fuera del dataset M5: la API devuelve 503 si el (item_id, store_id) no existe en la base de features histórica

---

## 3. Objetivos del Proyecto

### 3.1 Objetivo Principal

**Reducir costos operativos y maximizar ingresos mediante un sistema de forecasting preciso y optimización de inventario automatizada.**

### 3.2 Objetivos Específicos

> Nota: Los objetivos siguientes son **metas aspiracionales** para un despliegue real.  
> La demo actual prioriza reproducibilidad y visualización, no ejecución en producción.

#### Objetivos Técnicos:
1. **Desarrollar modelos de forecasting** con precisión superior al baseline:
   - Target: **WRMSSE < 0.60** (métrica oficial M5 Forecasting)
   - Target: **MAE < 2.5 unidades** por producto-día
   - Target: **MAPE < 15%** en agregados semanales

2. **Implementar forecasting jerárquico**:
   - Bottom-up: desde producto-tienda hasta nacional
   - Reconciliación de forecasts a todos los niveles
   - Coherencia en agregaciones

3. **Crear sistema de optimización de inventario**:
   - Cálculo de puntos de reorden óptimos
   - Optimización de cantidad económica de pedido (EOQ)
   - Minimización de costos totales (ordenar + almacenar + faltantes)

4. **Desarrollar pipeline end-to-end**:
   - ETL automatizado
   - Feature engineering reproducible
   - Training pipeline con MLflow tracking
   - API de predicción con FastAPI
   - Dashboard interactivo con Streamlit

#### Objetivos de Negocio:
1. **Reducir stockouts en 40-50%**:
   - Baseline: 8% de eventos de stockout
   - Target: ≤ 4% de eventos de stockout

2. **Optimizar niveles de inventario**:
   - Reducir inventario promedio en 15-20%
   - Mantener nivel de servicio ≥ 96%

3. **Mejorar eficiencia operacional**:
   - Reducir tiempo de planificación en 60% (automatización)
   - Alertas predictivas 7 días antes de posibles quiebres

4. **Generar valor medible (demo vs producción)**:
   - **Demo (basado en MAE real):** ~$46.7K/año por tienda (10 tiendas ≈ **$467K/año**)
   - **Producción (aspiracional):** reducción de costos de inventario 18-25% y +3-5% ventas por disponibilidad
   - Nota: el ROI demo se calcula con el MAE observado (ver Sección 7)

---

## 4. Métricas de Éxito

### 4.1 Métricas Técnicas (ML/DS)

| Métrica | Baseline | Target | Excepcional |
|---------|----------|--------|-------------|
| **WRMSSE** (Weighted Root Mean Squared Scaled Error) | 0.80 | < 0.60 | < 0.50 |
| **MAE** (Mean Absolute Error) | 3.5 unidades | < 2.5 unidades | < 2.0 unidades |
| **RMSE** (Root Mean Squared Error) | 5.2 unidades | < 4.0 unidades | < 3.5 unidades |
| **MAPE** (Mean Absolute Percentage Error) | 22% | < 15% | < 12% |
| **R²** | 0.65 | > 0.80 | > 0.85 |
| **Bias** | ±8% | ±3% | ±2% |

### 4.2 Métricas de Negocio

| KPI | Baseline | Target | Impacto Anual |
|-----|----------|--------|---------------|
| **Stockout Rate** | 8% | ≤ 4% | +$500K ventas/tienda |
| **Inventory Turnover** | 6.5x | 8.0x | -$800K inventario |
| **Service Level** | 92% | ≥ 96% | +3% satisfacción |
| **Forecast Accuracy** (agregado) | 70% | ≥ 85% | - |
| **Planning Time** | 40 hrs/semana | 15 hrs/semana | -$120K/año |
| **Obsolescence Rate** | 2.5% | < 1.5% | -$200K pérdidas |

### 4.3 Métricas de Sistema

| Métrica | Target |
|---------|--------|
| **Latencia API** | < 100ms (p95) |
| **Throughput** | > 1,000 predicciones/seg |
| **Uptime** | ≥ 99.5% |
| **Tiempo de retraining** | < 2 horas |
| **Data drift detection** | Alertas automáticas |

---

## 5. Stakeholders

### 5.1 Stakeholders Principales

| Rol | Nombre/Área | Interés | Nivel de Influencia |
|-----|-------------|---------|---------------------|
| **Sponsor Ejecutivo** | VP of Operations | ROI, reducción costos | Alto |
| **Usuario Final** | Store Managers (10 tiendas) | Alertas, recomendaciones accionables | Alto |
| **Usuario Final** | Inventory Planners | Forecasts precisos, optimización | Alto |
| **Technical Owner** | Data Science Team Lead | Calidad técnica, mantenibilidad | Medio |

### 5.2 Stakeholders Secundarios

| Rol | Interés |
|-----|---------|
| **Supply Chain** | Lead times, coordinación logística |
| **Finance** | Impacto en capital de trabajo |
| **IT** | Infraestructura, integración sistemas |
| **Category Managers** | Performance por categoría |

### 5.3 Necesidades por Stakeholder

**Store Managers necesitan:**
- Dashboard simple con alertas visuales
- Recomendaciones de reorden por producto
- Explicación de por qué aumentó/disminuyó forecast
- Alertas 7 días antes de stockout predicho

**Inventory Planners necesitan:**
- Forecast detallado por SKU-store-día
- Intervalos de confianza
- Análisis de sensibilidad (what-if)
- Exportación a Excel/CSV para análisis adicional

**VP Operations necesita:**
- KPIs consolidados (ROI, savings)
- Comparación baseline vs modelo
- Reportes ejecutivos semanales

---

## 6. Datos Disponibles

### 6.0 Dataset A/B/C (DVP-PRO)

- **Dataset A (raw)**: `data/raw/sales_train_validation.csv`
- **Dataset B (processed/train)**: `data/processed/train_data.csv`
- **Dataset C (processed/validation)**: `data/processed/valid_data.csv`

### 6.1 Dataset Principal: M5 Forecasting - Walmart

**Fuente**: Kaggle M5 Forecasting Competition
**Tamaño Total**: ~430 MB
**Período**: 2011-01-29 a 2016-06-19 (1,969 días / 5.4 años)

### 6.2 Archivos y Características

#### **sales_train_validation.csv** (114 MB)
```
Filas: 30,490 series temporales
Columnas: 1,919 (6 metadata + 1,913 días de ventas)
Granularidad: Diaria
Nivel: Producto × Tienda

Metadata:
- item_id: 3,049 productos únicos
- dept_id: 7 departamentos
- cat_id: 3 categorías (HOBBIES, FOODS, HOUSEHOLD)
- store_id: 10 tiendas (CA_1-4, TX_1-3, WI_1-3)
- state_id: 3 estados (CA, TX, WI)

Target: Ventas diarias (unidades vendidas)
```

#### **calendar.csv** (101 KB)
```
Filas: 1,969 días
Información:
- Fecha, día semana, mes, año
- Eventos especiales (Cultural, National, Religious, Sporting)
- SNAP eligibility por estado (programa asistencia alimentaria)
- Weeks (formato interno Walmart)
```

#### **sell_prices.csv** (194 MB)
```
Filas: 6.8M registros precio
Granularidad: Semanal (por wm_yr_wk)
Información:
- store_id, item_id
- sell_price (USD)
- Permite calcular: cambios precio, promociones, elasticidad
```

### 6.3 Calidad de Datos (Assessment Preliminar)

| Aspecto | Estado |
|---------|--------|
| **Completitud** | ✅ 100% (sin missing values en ventas) |
| **Consistencia** | ✅ Alta (validación preliminar exitosa) |
| **Exactitud** | ✅ Datos oficiales Walmart |
| **Actualidad** | ⚠️ Datos hasta 2016 (representativos pero no actuales) |
| **Relevancia** | ✅ Totalmente relevante para objetivo |

**Limitaciones identificadas:**
- Zero-inflated data: muchos días con 0 ventas (productos lentos)
- Ausencia de datos de competencia
- Sin información de marketing/promociones detalladas
- No incluye causas de stockouts históricos

---

## 7. Valor Esperado (ROI)

### 7.1 ROI Demo (derivado del error real del modelo)

Este cálculo vincula el desempeño observado (MAE) con un costo económico simple y replicable.

**Supuestos demo (conservadores):**
- Precio promedio: **$4.41** por unidad
- Ítems forecast por tienda/día: **100**
- Tiendas: **10**
- Días: **365**
- Costo de error: proporcional a `MAE × precio × items × días × tiendas`

**Cálculo:**
```
Baseline MAE: 0.9748
Modelo MAE:  0.6845

Costo baseline ≈ $1,569,121/año
Costo modelo  ≈ $1,101,873/año
Ahorro anual  ≈ $467,249 (10 tiendas)
```

**Ahorro por tienda (demo):** ~$46.7K/año

> Este ROI demo refleja valor **estimado** con el MAE real del modelo en validación.

### 7.2 Escalamiento (proyección prudente)

Si se escala a **500 tiendas** con el mismo ahorro por tienda:
- **ROI proyectado: ~$23.4M/año**

> Proyección conservadora basada en el ROI demo (no en objetivos aspiracionales).

### 7.3 Costos del Proyecto (referencia)

| Item | Costo Estimado |
|------|----------------|
| Desarrollo (3 meses) | $150K |
| Infraestructura (año 1) | $50K |
| Mantenimiento anual | $80K |
| **Total Año 1** | **$280K** |

**ROI Neto Año 1 (demo)**: $467K - $280K = **~$187K (≈67% ROI)**  
> En un despliegue real, el ROI puede ser mayor si se logra la reducción de stockouts e inventario objetivo.

---

## 8. Restricciones y Supuestos

### 8.1 Restricciones

#### Técnicas:
- Infraestructura: Desarrollo en laptop (16GB RAM, sin GPU requerido)
- Tiempo de ejecución: Training debe completarse en < 2 horas
- Latencia: API debe responder en < 100ms
- Datos históricos limitados: Solo hasta 2016

#### Temporales:
- Duración del proyecto: 8-10 semanas (para portafolio)
- Timeline para MVP: 4 semanas
- Timeline para producción completa: 8 semanas

#### Presupuestarias:
- Presupuesto: $0 (proyecto de portafolio)
- Uso de herramientas open-source exclusivamente
- Infraestructura local (sin cloud computing)

### 8.2 Supuestos

#### De Negocio:
1. Patrones de demanda históricos son representativos del futuro
2. Costos de inventario y stockout son constantes
3. Lead times de reposición son conocidos (asumimos 7 días)
4. No hay cambios drásticos en estrategia de negocio

#### Técnicos:
1. Datos están limpios y validados (por ser dataset oficial Kaggle)
2. Jerarquía de productos es estable
3. Precios en sell_prices.csv son completos y correctos
4. No hay efectos de canibalización entre productos

#### Operacionales:
1. Store managers adoptarán recomendaciones del sistema
2. Existe capacidad de ajustar órdenes basándose en forecasts
3. No hay restricciones de espacio de almacenamiento

---

## 9. Riesgos y Mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| **Overfitting en series con pocos datos** | Alta | Medio | Regularización, ensemble models, hierarchical forecasting |
| **Zero-inflated data** distorsiona métricas | Alta | Medio | Métricas customizadas, tratamiento especial productos lentos |
| **Drift entre datos 2016 y actualidad** | Media | Bajo | Enfoque en patrones generales, no valores absolutos |
| **Complejidad computacional** alta | Media | Medio | Optimización de código, muestreo estratégico para desarrollo |
| **Interpretabilidad de modelos complejos** | Media | Alto | SHAP values, feature importance, visualizaciones |

---

## 10. Criterios de Aceptación

### Para considerarse EXITOSO, el proyecto debe:

#### Fase de Desarrollo (MVP):
- ✅ EDA completo con insights documentados
- ✅ Pipeline de feature engineering reproducible
- ✅ Al menos 3 modelos baseline implementados y comparados
- ✅ Modelo final con WRMSSE < 0.60
- ✅ Validación cruzada implementada correctamente
- ✅ Código versionado en Git con commits descriptivos

#### Fase de Producción:
- ✅ API REST funcional con documentación Swagger
- ✅ Dashboard interactivo con métricas de negocio
- ✅ Sistema de logging y monitoreo básico
- ✅ Documentación técnica completa (README, docstrings)
- ✅ Tests unitarios para funciones críticas
- ✅ Docker containerization funcional

#### Fase de Portafolio:
- ✅ README profesional con badges y visualizaciones
- ✅ Model Card completo (modelo, métricas, limitaciones)
- ✅ Notebook de demostración ejecutable
- ✅ Presentación de resultados (slides/video)
- ✅ Cálculo de ROI y business case documentado

---

## 11. Timeline y Fases

### Fase 0: Definición del Problema ✅ COMPLETADA
**Duración**: 1 día
**Entregables**: Este documento

### Fase 1: Setup y Configuración
**Duración**: 1 día
**Entregables**: Estructura de proyecto, entorno virtual, Git init

### Fase 2: EDA y Data Quality Assessment
**Duración**: 4-5 días
**Entregables**: Notebook EDA, data quality report, insights preliminares

### Fase 3: Feature Engineering
**Duración**: 5-6 días
**Entregables**: Pipeline de features, feature catalog, validación

### Fase 4: Modelado Baseline
**Duración**: 4 días
**Entregables**: 3+ modelos baseline, comparación métricas, MLflow tracking

### Fase 5: Modelado Avanzado
**Duración**: 6-7 días
**Entregables**: Modelos optimizados, ensemble, hierarchical forecasting

### Fase 6: Evaluación y Validación
**Duración**: 3-4 días
**Entregables**: Validación rigurosa, análisis de errores, model interpretation

### Fase 7: Optimización de Inventario
**Duración**: 4-5 días
**Entregables**: Módulo de optimización, recomendaciones, cálculo ROI

### Fase 8: API y Dashboard
**Duración**: 5-6 días
**Entregables**: FastAPI funcional, dashboard Streamlit, documentación

### Fase 9: Deployment y Documentación
**Duración**: 3-4 días
**Entregables**: Docker, CI/CD básico, documentación completa

### Fase 10: Portafolio y Presentación
**Duración**: 3-4 días
**Entregables**: README profesional, presentación, video demo

**TOTAL ESTIMADO**: 8-10 semanas (tiempo parcial)

---

## 12. Próximos Pasos Inmediatos

### Acciones para Fase 1 (Setup):
1. ✅ Copiar datos de M5 a `data/raw/`
2. ⏳ Crear entorno virtual con Python 3.10+
3. ⏳ Instalar dependencias base (requirements.txt)
4. ⏳ Inicializar Git repository
5. ⏳ Crear config.yaml con parámetros del proyecto
6. ⏳ Crear notebook template 01_eda.ipynb

### Para Revisión/Aprobación:
- [ ] **Stakeholders**: Confirmar objetivos y métricas de negocio
- [ ] **Technical Lead**: Validar alcance técnico y stack
- [ ] **Sponsor**: Aprobar timeline y recursos

---

## 13. Referencias y Recursos

### Competencia M5 Forecasting:
- [M5 Competition Overview](https://www.kaggle.com/competitions/m5-forecasting-accuracy)
- [M5 Participants Guide](https://mofc.unic.ac.cy/m5-competition/)
- [Top Solutions Analysis](https://www.kaggle.com/c/m5-forecasting-accuracy/discussion)

### Literatura Técnica:
- Hyndman & Athanasopoulos - "Forecasting: Principles and Practice" (2021)
- Makridakis et al. - "The M5 Competition: Background, Organization, and Implementation" (2022)
- Wickramasuriya et al. - "Optimal Forecast Reconciliation" (2019)

### Herramientas y Frameworks:
- Prophet (Meta): Time series forecasting
- XGBoost/LightGBM: Gradient boosting para forecasting
- MLflow: Experiment tracking
- Streamlit: Dashboard interactivo

---

## 14. Firma y Aprobación

**Elaborado por**:
Ing. Daniel Varela Perez
Senior Data Scientist & ML Engineer
📧 bedaniele0@gmail.com
📱 +52 55 4189 3428

**Fecha**: 4 de Diciembre, 2024

**Versión del Documento**: 1.0 - Problem Statement Completo

---

## Anexo A: Glosario

| Término | Definición |
|---------|------------|
| **WRMSSE** | Weighted Root Mean Squared Scaled Error - Métrica oficial M5 que penaliza errores proporcionalmente al volumen de ventas |
| **SNAP** | Supplemental Nutrition Assistance Program - Programa de asistencia alimentaria de EE.UU. |
| **SKU** | Stock Keeping Unit - Identificador único de producto |
| **EOQ** | Economic Order Quantity - Cantidad óptima de pedido que minimiza costos totales |
| **Service Level** | Probabilidad de no tener stockout durante un ciclo de reposición |
| **Hierarchical Forecasting** | Técnica que garantiza coherencia entre forecasts agregados y desagregados |
| **Zero-inflated** | Datos con alta frecuencia de valores cero (productos sin ventas) |

---

**🎯 STATUS**: Problem Statement completado y listo para Fase 1 (Setup)

**NEXT**: Proceder con creación de entorno, configuración inicial y preparación de datos.
