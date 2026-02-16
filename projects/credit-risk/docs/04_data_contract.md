# Data Contract - Credit Risk Scoring (UCI Taiwan)

Autor: Ing. Daniel Varela Perez  
Email: bedaniele0@gmail.com  
Tel: +52 55 4189 3428  
Fecha: 04/02/2026  
Version: 1.0

---

## 1. Fuentes de Datos
- Fuente: UCI Taiwan - Default of Credit Card Clients (2005)
- Owner: Universidad Nacional de Taiwán / UCI ML Repository
- Frecuencia: Estática (snapshot)

## 2. Esquema

| Campo | Tipo | Descripcion | Reglas |
|---|---|---|---|
| ID | int | Identificador de cliente | no nulo, único |
| LIMIT_BAL | int | Límite de crédito | >= 0 |
| SEX | int | Sexo (1=H, 2=M) | valores {1,2} |
| EDUCATION | int | Nivel educativo | valores {0,1,2,3,4,5,6} |
| MARRIAGE | int | Estado civil | valores {0,1,2,3} |
| AGE | int | Edad | 18–100 |
| PAY_0..PAY_6 | int | Estatus de pago últimos 6 meses | [-2..8] |
| BILL_AMT1..BILL_AMT6 | int | Facturación mensual | >= 0 |
| PAY_AMT1..PAY_AMT6 | int | Pagos mensuales | >= 0 |
| default payment next month | int | Target (1=default, 0=non-default) | valores {0,1} |

## 3. Reglas de Calidad
- Missing permitido: 0% (tabla completa).
- Duplicados: ID único, duplicados = 0.
- Rango aceptable:
  - AGE: 18–100
  - SEX: {1,2}
  - EDUCATION: {0,1,2,3,4,5,6}
  - MARRIAGE: {0,1,2,3}
  - PAY_*: [-2..8]
  - BILL_AMT* y PAY_AMT*: >= 0

## 4. SLA
- Entrega: N/A (dataset estático)
- Retrasos: N/A

## 5. Cambios y Versionado
- Version actual: v1.0
- Responsable: Ing. Daniel Varela Perez

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
