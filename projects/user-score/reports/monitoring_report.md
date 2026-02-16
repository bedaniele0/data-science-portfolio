# Monitoring Report - F8 (SIMULADO)

**Proyecto/Modelo**: proyecto_user_score_ds
**Version**: v1.0
**Canal**: Batch diario
**Periodo auditado**: 30 dias (rolling)
**Frecuencia de revision**: mensual

**Autor**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428
**Framework**: DVP-MASTER
**Fecha**: 2026-02-06

---

## 1. Objetivos F0 (referencia)
- MAE <= 0.60
- R2 >= 0.50
- RMSE: minimizar

## 2. Estado actual (resumen)
- MAE: 0.452 ✅
- R2: 0.586 ✅
- RMSE: 0.676 (sin umbral definido)
- Cobertura de labels: 76% (38/50)

**Estado**: 🟡 Advertencia (drift alto en feature critica)

---

## 3. Umbrales de monitoreo (propuestos)

### 3.1 Performance del modelo
- MAE:
  - Warning: > 0.60
  - Critical: > 0.75
- R2:
  - Warning: < 0.50
  - Critical: < 0.35
- RMSE:
  - Warning: > 0.85
  - Critical: > 1.00

### 3.2 Drift de datos (PSI)
- meta_score (feature critica):
  - Warning: > 0.25
  - Critical: > 0.35
- esrb_rating:
  - Warning: > 0.25
  - Critical: > 0.35
- platform:
  - Warning: > 0.25
  - Critical: > 0.35

### 3.3 Calidad de datos
- Cobertura de labels:
  - Warning: < 85%
  - Critical: < 70%
- Missing rate en features clave:
  - Warning: > 20%
  - Critical: > 30%

---

## 4. Frecuencia y responsables
- Drift y performance: mensual
- Cobertura de labels: semanal
- Responsable tecnico: Data Science
- Responsable operativo: MLOps

---

## 5. Mini-Runbook (F8)

### Alerta A: PSI critico en meta_score
1) Verificar cambios en distribucion de meta_score por plataforma y genero.
2) Revisar si hay cambios upstream en data source.
3) Ejecutar evaluacion de performance por segmento.
4) Si PSI > 0.35 por 2 ventanas consecutivas, activar analisis de optimizacion.

### Alerta B: Degradacion de performance
1) Confirmar cobertura de labels y consistencia de joins.
2) Validar drift en features clave.
3) Ejecutar recalculo de MAE/R2 por ventana.
4) Si MAE > 0.75 o R2 < 0.35, preparar plan de remediacion.

### Alerta C: Baja cobertura de labels
1) Identificar retrasos en ingestion de labels.
2) Ajustar ventana de matching por event_date.
3) Si cobertura < 70% por 2 ventanas, escalar a owner de datos.

---

## 6. Decision recomendada
- Mantener modelo en AMARILLO (SIMULADO) con monitoreo reforzado.
- Activar seguimiento semanal de PSI para meta_score.
- Definir umbral oficial de RMSE.

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
