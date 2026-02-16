# Problem Statement - Credit Risk Scoring (UCI Taiwan)

**Autor**: Ing. Daniel Varela Perez  
**Email**: bedaniele0@gmail.com  
**Fecha**: 2026-02-04  
**Versión**: 1.0

---

## 1. Contexto de Negocio

### Situación Actual
Las decisiones de otorgamiento de crédito se basan en reglas estáticas y criterio de analistas. Esto limita la precisión, la escalabilidad y la trazabilidad del proceso. Con el dataset histórico, el **default rate base es 22.12%** (n=30,000).

### Problemática
No existe un scoring predictivo consistente para identificar clientes con alto riesgo de impago a corto plazo, lo que incrementa la morosidad y reduce el margen ajustado al riesgo.

---

## 2. Problema a Resolver

### Definición Clara (2-3 oraciones)
Predecir la probabilidad de incumplimiento del pago mínimo en el próximo mes, usando variables socioeconómicas y de comportamiento. Con base en esta probabilidad (PD), clasificar a los clientes en bandas de riesgo para apoyar decisiones de aprobación/revisión/rechazo.

### Alcance
**En Scope:**
- ✅ Scoring de riesgo de impago a 1 mes
- ✅ Bandas de riesgo (Aprobado/Revisión/Rechazo)
- ✅ Explicabilidad (SHAP) y fairness por género/educación

**Out of Scope:**
- ❌ Predicción de impago a 6-12 meses
- ❌ Estrategias de cobranza/recupero
- ❌ Pricing dinámico de crédito

---

## 3. Objetivos Específicos

### Objetivo de Negocio
Reducir el índice de morosidad en **≥ 12% relativo** y mejorar el margen ajustado al riesgo en **≥ 5%** dentro de 6-12 meses posteriores al despliegue.

### Objetivo Técnico
Desarrollar un modelo con desempeño mínimo:
- **AUC-ROC ≥ 0.80**
- **KS ≥ 0.30**
- **Recall (clase 1) ≥ 0.70**
- **Precision (clase 1) ≥ 0.30**
- **Brier Score ≤ 0.20**

---

## 4. Métricas de Éxito

### Métricas de Negocio
| Métrica | Baseline Actual | Objetivo | Medición |
|---------|------------------|----------|----------|
| Índice de morosidad | 22.12% (proxy dataset) | 19.46% (−12% relativo) | Mensual |
| Margen ajustado al riesgo | TBD | +5% | Trimestral |
| Tiempo de respuesta del scoring | N/A | < 200 ms | p95 |

### Métricas Técnicas
| Métrica | Baseline | Objetivo | Criticidad |
|---------|----------|----------|------------|
| AUC-ROC | 0.50 (random) | ≥ 0.80 | Alta |
| KS | 0.00 (random) | ≥ 0.30 | Alta |
| Recall (clase 1) | 0.00 (random) | ≥ 0.70 | Alta |
| Precision (clase 1) | 0.00 (random) | ≥ 0.30 | Media |
| Brier Score | 0.25 (naive p=0.5) | ≤ 0.20 | Media |

### Criterio de Éxito
El proyecto se considera exitoso si:
1. Se cumplen todas las métricas técnicas mínimas en validación.
2. Se observa reducción de morosidad ≥ 12% relativa en producción.
3. El scoring opera con latencia < 200 ms p95.

---

## 5. Stakeholders

### Sponsor del Proyecto
- **Nombre**: Ing. Daniel Varela Perez
- **Rol**: Senior Data Science
- **Responsabilidad**: Sponsor técnico y aprobación de go-live del modelo

### Usuarios Finales
- **Equipo**: Analistas de Riesgo y Cobranza
- **Uso**: Priorización y decisión de aprobación/revisión/rechazo
- **Expectativas**: Mejor separación de riesgos y trazabilidad

### Equipo Técnico
| Rol | Nombre | Responsabilidad |
|-----|--------|-----------------|
| Data Scientist | Daniel Varela | Modelado y validación |
| Data Engineer | TBD | Pipeline de datos |
| MLOps Engineer | TBD | Deployment y monitoreo |
| Business Owner | CRO (placeholder) | Aprobación de negocio |

### Matriz RACI
| Actividad | Data Scientist | Data Engineer | MLOps | Negocio |
|-----------|----------------|---------------|-------|---------|
| Definir problema | C | C | I | R/A |
| EDA | R/A | C | I | C |
| Feature Engineering | R/A | R | I | C |
| Modelado | R/A | I | C | C |
| Deployment | C | R | R/A | I |
| Monitoreo | C | C | R/A | I |

---

## 6. Datos Disponibles

### Fuentes de Datos
| Fuente | Descripción | Actualización | Acceso |
|--------|-------------|---------------|--------|
| UCI Taiwan 2005 | Default of Credit Card Clients | Estático | ✅ Disponible |

### Datos Requeridos vs Disponibles
- **Requeridos**: historial de pagos, límites de crédito, demográficos básicos
- **Disponibles**: `data/raw/default of credit card clients.csv` ✅
- **Gap**: no hay variables de comportamiento digital o ingresos verificados

---

## 7. Valor Esperado (ROI)

### Estimación preliminar (requiere validación financiera)
```
Clientes totales: 30,000
Default baseline: 22.12% -> 6,636 defaults
Reducción objetivo: 12% relativo -> 796 defaults evitados
Beneficio unitario por default evitado: TBD
Beneficio anual estimado: 796 × costo_default (TBD)
```

**ROI y Payback**: TBD hasta confirmar costos/beneficios reales con negocio.

---

## 8. Restricciones y Supuestos

### Restricciones
- Latencia de scoring < 200 ms (p95)
- Explicabilidad obligatoria (SHAP)
- Fairness por género y educación

### Supuestos
- ✅ Datos históricos son representativos
- ✅ Definición de default = `default payment next month`
- ✅ Split 80/20 y CV 5-fold

---

## 9. Timeline y Fases

| Fase | Duración | Entregables | Responsable |
|------|----------|-------------|-------------|
| F0 - Contexto | 1 semana | Problem statement, business case | DS |
| F1 - Setup | 3 días | Entorno y estructura | DS |
| F2 - Arquitectura | 1 semana | Diseño técnico | DS/DE |
| F3 - EDA | 2 semanas | EDA report | DS |
| F4 - Features | 2 semanas | Feature catalog | DS/DE |
| F5 - Modelado | 3 semanas | Modelos candidatos | DS |
| F6 - Validación | 1 semana | Model evaluation | DS |
| F7 - Deployment | 2 semanas | API/Batch en prod | MLOps/DS |

---

## 10. Decisiones que se Tomarán
1. Aprobación automática si PD < 20%
2. Revisión manual si 20% ≤ PD < 50%
3. Rechazo si PD ≥ 50%

---

## 11. Criterios de Aceptación

### Técnicos
- [ ] AUC-ROC ≥ 0.80
- [ ] KS ≥ 0.30
- [ ] Gap train-val < 5%
- [ ] Fairness audit aprobado

### Negocio
- [ ] Morosidad −12% relativa
- [ ] Margen +5%

### Operacionales
- [ ] Latencia < 200 ms (p95)
- [ ] Monitoreo de drift activo

---

## 12. Próximos Pasos
1. Validar acceso y calidad de datos (F1/F2)
2. Ejecutar EDA (F3)
3. Definir feature catalog (F4)

---

## 13. Aprobaciones

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Sponsor | Ing. Daniel Varela Perez | __________ | 2026-02-04 |
| Data Science Lead | Ing. Daniel Varela Perez | __________ | 2026-02-04 |

---

## 14. Control de Cambios
| Versión | Fecha | Cambio | Autor |
|---------|-------|--------|-------|
| 1.0 | 2026-02-04 | Versión inicial | Ing. Daniel Varela Perez |

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
