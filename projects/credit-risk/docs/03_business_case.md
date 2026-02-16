# Business Case - Credit Risk Scoring (UCI Taiwan)

**Autor**: Ing. Daniel Varela Perez  
**Email**: bedaniele0@gmail.com  
**Fecha**: 2026-02-04  
**Versión**: 1.0

---

## 1. Resumen Ejecutivo
- Problema: alta morosidad por decisiones de crédito basadas en reglas estáticas.
- Solucion propuesta: modelo de scoring predictivo con bandas de riesgo y explicabilidad.
- Impacto estimado: −12% relativo de morosidad y +5% de margen ajustado al riesgo.

## 2. Contexto y Justificacion
- Situacion actual: decisiones manuales con baja trazabilidad y performance desigual.
- Oportunidad: usar datos históricos para priorizar decisiones de aprobación/revisión/rechazo.
- Por que ahora: existe dataset histórico con 30,000 registros y variables relevantes.

## 3. Alcance
- En scope: scoring 1 mes, bandas de riesgo, XAI, fairness.
- Out of scope: cobranza, pricing dinámico, horizonte > 1 mes.

## 4. Opciones Evaluadas
| Opcion | Descripcion | Pros | Contras | Decision |
|---|---|---|---|---|
| A | Reglas estáticas | Simple, interpretable | Baja precisión | No |
| B | Modelo ML (LogReg/GBM) | Mejor performance y calibración | Requiere MLOps | Si |

## 5. Costos (estimación preliminar)
| Item | Costo | Frecuencia | Notas |
|---|---|---|---|
| Data Scientist (1.5 meses) | USD 7,500 | unico | sup. 5,000/mes |
| Data Engineer (0.5 meses) | USD 2,500 | unico | setup data |
| MLOps (0.5 meses) | USD 2,500 | unico | despliegue/monitoring |
| Infraestructura | USD 300 | mensual | dev + monitoring |

## 6. Beneficios (estimación preliminar)
| Beneficio | Metrica | Valor estimado | Fuente |
|---|---|---|---|
| Defaults evitados | −12% relativo | 796 defaults evitados | baseline 22.12% |
| Reducción pérdida | USD TBD | TBD | requiere costo por default |

## 7. ROI
- Formula: (Beneficio - Costo) / Costo
- ROI estimado: TBD (requiere validar costo por default)
- Payback: TBD

## 8. Riesgos y Mitigaciones
| Riesgo | Impacto | Probabilidad | Mitigacion | Owner |
|---|---|---|---|---|
| Drift temporal | Alto | Media | monitoreo PSI + recalibración | MLOps |
| Sesgo por género/educación | Medio | Media | fairness audit | DS |
| Beneficio económico no validado | Alto | Media | validar con finanzas | Sponsor |

## 9. Timeline
- Inicio: 04/02/2026
- Fases clave: F0-F7 (8-10 semanas)
- Entrega: 15/04/2026 (estimado)

## 10. Aprobacion
- Sponsor: Ing. Daniel Varela Perez
- Fecha: 2026-02-04
- Decision: Go (condicionado a validación de ROI)

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
