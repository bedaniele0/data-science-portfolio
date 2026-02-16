# Design Architecture - Prediccion de User Score

**Autor**: Ing. Daniel Varela Perez  
**Email**: bedaniele0@gmail.com  
**Tel**: +52 55 4189 3428  
**Fecha**: 2026-02-06  
**Versión**: 1.0  

---

## 1. Overview
Arquitectura batch para ingesta, features, entrenamiento y scoring.  
El despliegue es local/demo con scripts y artefactos en repositorio.

## 2. Componentes
- **Ingesta**: lectura de `data/data.csv`
- **Procesamiento**: limpieza y features en `src/`
- **Modelado**: entrenamiento y evaluación en `src/`
- **Artefactos**: modelos en `models/`, métricas en `reports/`
- **Serving (demo)**: batch scoring sobre `data/prod/input.csv`

## 3. Flujo de Datos
1) raw → processed  
2) processed → features  
3) features → models  
4) models → predictions  

## 4. Interfaces
- Input: `data/prod/input.csv`
- Output: `data/prod/predictions.csv`

## 5. Versionado
- Datos: `data/`
- Modelos: `models/`
- Reportes: `reports/`
