# API Validation Guide - Paso a Paso

**Author**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Date**: December 5, 2024

---

## 🎯 Objetivo

Validar que la API de Walmart Demand Forecasting funciona correctamente en tu ambiente local.

---

## ✅ Checklist Pre-Validación

Antes de empezar, asegúrate de tener:

- [ ] Docker Desktop instalado y **CORRIENDO** ⚠️
- [ ] Modelo entrenado (`models/lightgbm_model.pkl` existe)
- [ ] Feature catalog (`data/processed/feature_catalog.txt` existe)
- [ ] Puerto 8000 libre (no usado por otra app)

---

## 🚀 Paso 1: Iniciar Docker Desktop

### macOS
1. Abre **Docker Desktop** desde Aplicaciones
2. Espera a que aparezca el icono de Docker en la barra de menú
3. Verifica que dice "Docker Desktop is running"

### Verificar que Docker está corriendo:
```bash
docker ps
```

**Output esperado**: Lista de containers (puede estar vacía)

**Si da error**: Docker no está corriendo. Inicia Docker Desktop primero.

---

## 🏗️ Paso 2: Levantar la API

### Opción A: Con Docker Compose (Recomendado)

```bash
# Navegar al proyecto
cd /Users/danielevarella/Desktop/walmart-demand-forecasting

# Levantar API (primera vez puede tardar 2-3 minutos)
docker-compose up -d --build
```

**Output esperado**:
```
[+] Building 45.3s (12/12) FINISHED
[+] Running 2/2
 ✔ Network walmart-network    Created
 ✔ Container walmart-forecasting-api  Started
```

### Verificar que está corriendo:
```bash
docker ps
```

**Deberías ver**:
```
CONTAINER ID   IMAGE                    STATUS         PORTS
abc123def456   walmart-forecasting-api  Up 10 seconds  0.0.0.0:8000->8000/tcp
```

### Ver logs en tiempo real:
```bash
docker-compose logs -f
```

**Presiona Ctrl+C para salir de los logs**

---

## 🧪 Paso 3: Probar la API

### Test 1: Health Check ✅

```bash
curl http://localhost:8000/health
```

**Output esperado**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0",
  "uptime_seconds": 45.23,
  "timestamp": "2024-12-05T15:30:00Z"
}
```

✅ **Si ves `"model_loaded": true`** → ¡Éxito!
❌ **Si ves `"model_loaded": false`** → Problema con el modelo

---

### Test 2: Root Endpoint

```bash
curl http://localhost:8000/
```

**Output esperado**:
```json
{
  "message": "Walmart Demand Forecasting API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health",
  "model_info": "/model/info"
}
```

---

### Test 3: Model Info

```bash
curl http://localhost:8000/model/info
```

**Output esperado**:
```json
{
  "model_name": "Walmart Demand Forecasting LightGBM",
  "model_version": "1.0.0",
  "model_type": "LightGBM",
  "training_date": "2024-12-05",
  "features_count": 80,
  "performance_metrics": {
    "mae": 0.6845,
    "rmse": 3.9554,
    "mape": 52.75
  }
}
```

---

### Test 4: Single Prediction 🎯

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": "FOODS_1_001_CA_1",
    "store_id": "CA_1",
    "date": "2016-05-01"
  }'
```

**Output esperado**:
```json
{
  "item_id": "FOODS_1_001_CA_1",
  "store_id": "CA_1",
  "date": "2016-05-01",
  "predicted_sales": 2.34,
  "prediction_interval": {
    "lower": 0.00,
    "upper": 10.12
  },
  "model_version": "1.0.0",
  "timestamp": "2024-12-05T15:31:00Z"
}
```

⚠️ **Nota**: La predicción usa features mock actualmente, por lo que el valor no es real.

---

### Test 5: Batch Predictions

```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"item_id": "FOODS_1_001_CA_1", "store_id": "CA_1", "date": "2016-05-01"},
      {"item_id": "FOODS_1_002_CA_1", "store_id": "CA_1", "date": "2016-05-01"}
    ]
  }'
```

**Output esperado**:
```json
{
  "predictions": [...],
  "total_items": 2,
  "processing_time_ms": 52.45
}
```

---

### Test 6: Feature Importance

```bash
curl http://localhost:8000/model/features/importance?top_n=5
```

**Output esperado**:
```json
{
  "top_n": 5,
  "features": [
    {"feature": "sales_rolling_mean_7", "importance": 509.0},
    {"feature": "sales_lag_3", "importance": 292.0},
    ...
  ],
  "timestamp": "2024-12-05T15:32:00Z"
}
```

---

## 📚 Paso 4: Documentación Interactiva

Abre tu navegador y visita:

```
http://localhost:8000/docs
```

Deberías ver **Swagger UI** con todos los endpoints documentados.

### Probar desde Swagger:
1. Click en cualquier endpoint (ej: POST /predict)
2. Click "Try it out"
3. Modifica el JSON de ejemplo
4. Click "Execute"
5. Ver la respuesta

---

## 🧪 Paso 5: Ejecutar Notebook Demo

### Opción 1: Jupyter Notebook

```bash
# Activar virtual environment
source venv/bin/activate

# Iniciar Jupyter
jupyter notebook notebooks/06_api_demo.ipynb
```

### Opción 2: VS Code

1. Abrir `notebooks/06_api_demo.ipynb` en VS Code
2. Seleccionar kernel de Python 3
3. Ejecutar todas las celdas (Run All)

**El notebook hará**:
- ✅ Probar todos los endpoints
- ✅ Medir tiempos de respuesta
- ✅ Test de error handling
- ✅ Benchmark de performance
- ✅ Generar visualizaciones
- ✅ Crear reporte de resultados

---

## 🔍 Paso 6: Verificar Logs

### Ver logs del container:
```bash
docker-compose logs api
```

### Ver logs en tiempo real:
```bash
docker-compose logs -f api
```

**Buscar en logs**:
- ✅ "Model loaded successfully"
- ✅ "API ready to serve requests"
- ✅ Status codes 200 (éxito)
- ❌ Errores o warnings

---

## 🛑 Paso 7: Detener la API

Cuando termines la validación:

```bash
docker-compose down
```

**Output esperado**:
```
[+] Running 2/2
 ✔ Container walmart-forecasting-api  Removed
 ✔ Network walmart-network            Removed
```

---

## 🐛 Troubleshooting

### Problema 1: "Cannot connect to Docker daemon"

**Causa**: Docker Desktop no está corriendo

**Solución**:
1. Abrir Docker Desktop
2. Esperar a que inicie completamente
3. Intentar de nuevo

---

### Problema 2: "Port 8000 already in use"

**Causa**: Otro proceso usa el puerto 8000

**Solución**:
```bash
# Ver qué está usando el puerto
lsof -i :8000

# Matar el proceso (reemplaza PID)
kill -9 <PID>

# O cambiar el puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usar puerto 8001 en lugar de 8000
```

---

### Problema 3: "model_loaded: false"

**Causa**: Modelo no se cargó correctamente

**Solución**:
```bash
# Verificar que modelo existe
ls -lh models/lightgbm_model.pkl

# Ver logs del container
docker-compose logs api | grep -i "model"

# Reintentar
docker-compose restart api
```

---

### Problema 4: Timeout en requests

**Causa**: Container aún está iniciando

**Solución**:
```bash
# Esperar 30 segundos después de docker-compose up
sleep 30

# Verificar health
curl http://localhost:8000/health
```

---

## ✅ Checklist de Validación

Marca cada test que pases:

- [ ] Docker Desktop corriendo
- [ ] `docker-compose up -d` exitoso
- [ ] `docker ps` muestra container corriendo
- [ ] Health check retorna `"model_loaded": true`
- [ ] Root endpoint responde
- [ ] Model info retorna métricas
- [ ] Single prediction funciona
- [ ] Batch predictions funciona
- [ ] Feature importance retorna features
- [ ] Swagger UI accesible en /docs
- [ ] Notebook demo ejecuta sin errores
- [ ] Logs no muestran errores críticos

**Si marcaste 12/12**: ✅ **¡API VALIDADA!**

---

## 📊 Resultados Esperados

### Performance Benchmarks

| Métrica | Valor Esperado |
|---------|---------------|
| Health check | <20ms |
| Single prediction | <100ms |
| Batch 10 items | <500ms |
| Batch 100 items | <2000ms |

### Success Rate

- **Target**: 100% de tests pasando
- **Acceptable**: >95% de tests pasando
- **Issue**: <95% de tests pasando → Investigar

---

## 📝 Reporte de Validación

Después de ejecutar el notebook, encontrarás:

```
reports/api_test_report_YYYYMMDD_HHMMSS.csv
```

Este archivo contiene:
- Endpoints testeados
- Status de cada test
- Tiempos de respuesta
- Errores encontrados

---

## 🎯 Próximos Pasos

Una vez validado exitosamente:

1. ✅ **Documentar findings** en `docs/`
2. ✅ **Crear screenshots** de Swagger UI
3. ✅ **Decidir**: ¿Implementar features reales? ¿O pasar a monitoring?

---

## 💡 Tips

### Para desarrollo:

```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Reiniciar API rápidamente
docker-compose restart api

# Rebuild después de cambios
docker-compose up -d --build

# Entrar al container (debugging)
docker exec -it walmart-forecasting-api /bin/bash
```

### Para testing:

```bash
# Instalar herramientas de testing
pip install httpie  # Better curl alternative

# Usar httpie
http http://localhost:8000/health

# JSON formatting con jq
curl http://localhost:8000/health | jq
```

---

## 📞 Soporte

Si encuentras problemas:

**Author**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428

---

**Última actualización**: December 5, 2024
**Versión**: 1.0.0
**Status**: ✅ Ready for validation
