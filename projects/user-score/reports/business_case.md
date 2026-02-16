# Business Case - Prediccion de User Score

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2026-02-06
Version: 1.0

---

## 1. Resumen Ejecutivo
- Problema: No existe analisis ni modelo para anticipar el `user_score`.
- Solucion propuesta: EDA + modelo de regresion baseline con mejoras ligeras.
- Impacto estimado: Insights accionables y caso de portafolio reproducible.

## 2. Contexto y Justificacion
- Situacion actual: Dataset disponible sin explotacion analitica.
- Oportunidad: Entender factores que afectan percepcion del usuario.
- Por que ahora: Caso ideal para generar portafolio y pipeline reusable.

## 3. Alcance
- En scope: EDA, limpieza basica, feature engineering, baseline + mejora, reporte.
- Out of scope: Despliegue, MLOps, dashboards avanzados.

## 4. Opciones Evaluadas
| Opcion | Descripcion | Pros | Contras | Decision |
|---|---|---|---|---|
| A | Regresion lineal + features basicas | Simple, interpretable | Puede subajustar | Si |
| B | RandomForest Regressor | Captura no linealidad | Menor interpretabilidad | Si |

## 5. Costos
| Item | Costo | Frecuencia | Notas |
|---|---|---|---|
| Personal | 3-4 dias | Unico | Proyecto individual |
| Infra | 0 | Unico | Local |

## 6. Beneficios
| Beneficio | Metrica | Valor estimado | Fuente |
|---|---|---|---|
| Insights accionables | Top drivers | Cualitativo | Reporte |
| Caso de portafolio | Documento completo | Alto | Entregables |

## 7. ROI
- Formula: (Beneficio - Costo) / Costo
- ROI estimado: N/A (cualitativo alto)
- Payback: Inmediato (portafolio)

## 8. Riesgos y Mitigaciones
| Riesgo | Impacto | Probabilidad | Mitigacion | Owner |
|---|---|---|---|---|
| Pocos datos utiles | Medio | Media | Feature engineering basico | DS |
| Objetivos tecnicos no alcanzados | Medio | Media | Ajuste de modelos y features | DS |

## 9. Timeline
- Inicio: 19/01/2026
- Fases clave: F0, F3, F5, F6, F9
- Entrega: 22/01/2026 (estimado)

## 10. Aprobacion
- Sponsor: N/A
- Fecha: 2026-02-06
- Decision: Go
