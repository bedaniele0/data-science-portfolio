# F1 - Setup del Proyecto - Fraud Detection

## OS Validado

- macOS Sequoia
**Autor:** Ing. Daniel Varela Pérez
**Email:** bedaniele0@gmail.com
**Metodología:** DVP-PRO (Fase 1)

## 1. Objetivo de la Fase

Configurar el entorno de desarrollo, instalar dependencias y validar que todos los componentes del proyecto están listos para desarrollo.

## 2. Requisitos del Sistema

### Hardware Mínimo
- CPU: 4 cores
- RAM: 8 GB
- Disco: 5 GB disponibles

### Software Requerido
- Python 3.10+
- pip (gestor de paquetes)
- Git
- (Opcional) Docker 20.10+

## 3. Instalación del Entorno

### Opción 1: Instalación Estándar

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/fraud_detection.git
cd fraud_detection

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Actualizar pip
pip install --upgrade pip setuptools wheel

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Instalar paquete en modo desarrollo
pip install -e .
```

### Opción 2: Instalación con Docker

```bash
# 1. Construir imagen
docker build -t fraud-detection:latest .

# 2. Ejecutar contenedor
docker run -p 8000:8000 fraud-detection:latest
```

## 4. Verificación de Instalación

### Tests
```bash
# Ejecutar suite completa
pytest -v

# Resultado esperado: 34/34 tests pasando ✅
```

### API
```bash
# Levantar API
python -m uvicorn api.main:app --reload

# Verificar en navegador: http://localhost:8000/docs
```

### Dashboard
```bash
# Levantar dashboard
python -m streamlit run dashboard/fraud_detection_dashboard.py

# Verificar en navegador: http://localhost:8501
```

## 5. Estructura de Directorios Creada

```
fraud_detection/
├── api/                    # API REST
├── dashboard/              # Dashboard Streamlit
├── src/                    # Código fuente
│   ├── models/            # ML pipeline
│   ├── monitoring/        # Drift detection
│   ├── data/              # Data processing
│   └── utils/             # Utilidades
├── data/
│   ├── raw/               # Datos originales
│   └── processed/         # Datos procesados
├── models/                # Modelos entrenados
├── tests/                 # Suite de tests
├── docs/                  # Documentación DVP-PRO
├── reports/               # Reportes y métricas
└── config/                # Configuración
```

## 6. Configuración de Variables de Entorno

Crear archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Variables críticas:
```
MODEL_PATH=models/improved_recall_threshold_model.pkl
THRESHOLD=0.30
JWT_SECRET=your-secret-key-here
LOG_LEVEL=INFO
```

## 7. Datos Iniciales

Los datos procesados ya están disponibles en:
- `data/processed/train_clean.parquet/`
- `data/processed/validation_clean.parquet/`
- `data/processed/test_clean.parquet/`

Fuente: [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud)

## 8. Checklist de Setup Completado

- [x] Python 3.10+ instalado
- [x] Entorno virtual creado y activado
- [x] Dependencias instaladas (`requirements.txt`)
- [x] Paquete instalado en modo desarrollo
- [x] Tests ejecutados (34/34 pasando)
- [x] API funcional (http://localhost:8000/docs)
- [x] Dashboard funcional (http://localhost:8501)
- [x] Modelo pre-entrenado disponible
- [x] Variables de entorno configuradas

## 9. Troubleshooting

### Error: "Module not found"
```bash
# Reinstalar paquete
pip install -e .
```

### Error: "Port already in use"
```bash
# API en otro puerto
uvicorn api.main:app --port 8001

# Dashboard en otro puerto
streamlit run dashboard/fraud_detection_dashboard.py --server.port 8502
```

### Error: Tests fallan
```bash
# Verificar entorno activo
which python  # Debe apuntar a venv/bin/python

# Reinstalar dependencias de testing
pip install pytest pytest-cov pytest-mock httpx
```

## 10. Próximos Pasos

Una vez completado el setup:
1. Revisar F2 (Arquitectura)
2. Explorar F3 (EDA)
3. Entrenar modelo (F5)
4. Evaluar resultados (F6)

## 11. Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [pytest Documentation](https://docs.pytest.org)
- [Docker Documentation](https://docs.docker.com)
