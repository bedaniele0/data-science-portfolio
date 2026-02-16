# 💳 Dashboard de Detección de Fraude - Guía de Usuario

## 📊 Información del Sistema
**Desarrollado por**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Teléfono**: +52 55 4189 3428
**Fecha**: 24 de Septiembre, 2025

---

## 🎯 Descripción General

El Dashboard de Detección de Fraude es una aplicación web interactiva construida con **Streamlit** que proporciona una interfaz gráfica completa para el sistema de detección de fraude bancario. Permite análisis individual, procesamiento batch, monitoreo en tiempo real y configuración avanzada del sistema.

---

## 🚀 Instalación y Configuración

### Requisitos Previos
```bash
# Instalar dependencias
pip install streamlit plotly pandas numpy scikit-learn joblib

# O usar requirements.txt
pip install -r requirements.txt
```

### Archivos Necesarios
- `models/improved_recall_threshold_model.pkl` (modelo optimizado)
- `models/threshold_config.json` (configuración del threshold)
- `dashboard/fraud_detection_dashboard.py` (aplicación principal)

### Lanzamiento
```bash
# Opción 1: Script automático
python run_dashboard.py

# Opción 2: Lanzamiento manual
streamlit run dashboard/fraud_detection_dashboard.py --server.port 8501
```

### Acceso
- **URL**: http://localhost:8501
- **Puerto**: 8501 (configurable)

---

## 📱 Funcionalidades del Dashboard

### 🔍 **Tab 1: Predicción Individual**

**Propósito**: Analizar transacciones individuales en tiempo real.

**Características**:
- ✅ Formulario intuitivo para ingreso de datos
- ✅ Datos de muestra para testing rápido
- ✅ Threshold ajustable en tiempo real
- ✅ Visualización con gauge de probabilidad
- ✅ Análisis de features principales
- ✅ Recomendaciones automáticas

**Uso**:
1. Ingresa datos de la transacción (monto, variables PCA)
2. Ajusta el threshold si es necesario (default: 0.300)
3. Clic en "Analizar Transacción"
4. Revisa resultados: gauge, métricas, recomendaciones

**Ejemplo de Entrada**:
- Monto: $1500.00
- V1: -2.5, V2: 3.1, V3: -1.8
- Threshold: 0.30

**Salida Esperada**:
- Probabilidad de Fraude: 85.2%
- Predicción: FRAUDE
- Nivel de Riesgo: ALTO

### 📈 **Tab 2: Análisis Batch**

**Propósito**: Procesar múltiples transacciones simultáneamente.

**Características**:
- ✅ Carga de archivos CSV
- ✅ Generación de datos demo (10-1000 transacciones)
- ✅ Procesamiento con barra de progreso
- ✅ Gráficos de distribución automáticos
- ✅ Filtros dinámicos de resultados
- ✅ Descarga de resultados en CSV

**Formato CSV Requerido**:
```csv
Amount,V1,V2,V3,V4,V5,...,V28
150.00,-1.2,2.3,-0.8,1.1,-0.5,...,0.2
2500.00,-3.1,4.2,-2.1,2.8,-1.9,...,1.1
```

**Métricas Calculadas**:
- Total de transacciones procesadas
- Número de fraudes detectados
- Tasa de fraude del lote
- Score de riesgo promedio

### 📊 **Tab 3: Métricas en Tiempo Real**

**Propósito**: Monitorear el sistema de forma continua.

**Características**:
- ✅ Auto-refresh cada 5 segundos (opcional)
- ✅ KPIs en tiempo real (24 horas)
- ✅ Gráficos de tendencias por hora
- ✅ Sistema de alertas automáticas
- ✅ Estadísticas del modelo
- ✅ Distribución de scores de riesgo

**KPIs Monitoreados**:
- Transacciones por hora
- Fraudes detectados
- Tasa de fraude promedio
- Tiempo de respuesta del modelo

**Sistema de Alertas**:
- 🟡 **Alerta Media**: >3 fraudes en última hora
- 🔴 **Alerta Alta**: Tasa de fraude >0.5%

### ⚙️ **Tab 4: Configuración**

**Propósito**: Ajustar parámetros del sistema.

**Características**:
- ✅ Ajuste dinámico del threshold
- ✅ Estimación de impacto en métricas
- ✅ Información detallada del modelo
- ✅ Herramientas de mantenimiento
- ✅ Test de conexión

**Threshold Adjustment**:
- **Bajo (0.10)**: Más sensible, detecta más fraudes, más falsas alarmas
- **Óptimo (0.30)**: Balance ideal precision-recall
- **Alto (0.50)**: Menos sensible, menos falsas alarmas, puede perder fraudes

---

## 🎯 Casos de Uso Principales

### 1. **Análisis de Transacción Sospechosa**
```
Escenario: Cliente reporta cargo no reconocido
Proceso:
1. Tab "Predicción Individual"
2. Ingresar datos de la transacción
3. Revisar probabilidad y nivel de riesgo
4. Seguir recomendaciones del sistema
```

### 2. **Procesamiento de Lote Nocturno**
```
Escenario: Análisis batch de todas las transacciones del día
Proceso:
1. Tab "Análisis Batch"
2. Subir CSV con transacciones del día
3. Procesar con threshold estándar
4. Descargar reporte de fraudes detectados
5. Enviar a equipo de investigación
```

### 3. **Monitoreo Operacional**
```
Escenario: Supervisor monitoreando actividad fraudulenta
Proceso:
1. Tab "Métricas en Tiempo Real"
2. Activar auto-refresh
3. Monitorear KPIs y alertas
4. Investigar picos de actividad sospechosa
```

### 4. **Ajuste de Sensibilidad**
```
Escenario: Demasiadas falsas alarmas reportadas
Proceso:
1. Tab "Configuración"
2. Aumentar threshold (ej: 0.30 → 0.35)
3. Revisar impacto estimado
4. Guardar nueva configuración
5. Monitorear resultados por 1-2 días
```

---

## 📊 Métricas de Performance

### Sistema Actual (Threshold 0.30)
- **Precision**: 93.62%
- **Recall**: 72.13%
- **F1-Score**: 81.48%
- **Accuracy**: 99.96%

### Comparativa vs Validación
- Métricas estables entre validation y test (sin cambios relevantes)

---

## 🛠️ Troubleshooting

### Problemas Comunes

**1. Error: "No se pudo cargar el modelo"**
```
Solución:
- Verificar que existe: models/improved_recall_threshold_model.pkl
- Si no existe, ejecutar notebooks 03 y 04
- Verificar permisos de lectura del archivo
```

**2. Dashboard no carga**
```
Solución:
- Verificar puerto 8501 disponible
- Instalar dependencias: pip install streamlit plotly
- Usar script: python run_dashboard.py
```

**3. Error en análisis batch**
```
Solución:
- Verificar formato CSV correcto
- Asegurar columnas V1-V28 presentes
- Verificar valores numéricos válidos
```

**4. Métricas en tiempo real no actualizan**
```
Solución:
- Activar checkbox "Actualización Automática"
- Refrescar página manualmente
- Verificar conexión a internet
```

### Logs y Debugging

**Habilitar logs detallados**:
```bash
streamlit run dashboard/fraud_detection_dashboard.py --logger.level debug
```

**Verificar estado del modelo**:
- Tab "Configuración" → "Test de Conexión"

---

## 🔧 Customización Avanzada

### Modificar Thresholds por Defecto
```python
# En fraud_detection_dashboard.py, línea ~45
config = {'best_threshold': 0.30}  # Cambiar valor
```

### Añadir Nuevas Métricas
```python
# En Tab 3, añadir nuevos KPIs
new_metric = calculate_custom_metric(data)
st.metric("Nueva Métrica", new_metric)
```

### Personalizar Alertas
```python
# Modificar umbrales de alertas
if fraude_rate > 0.3:  # Cambiar de 0.5 a 0.3
    alerts.append({'tipo': 'ALTA', 'mensaje': '...'})
```

---

## 📈 Roadmap Futuro

### Funcionalidades Planificadas
- ✨ **Integración con APIs bancarias reales**
- ✨ **Alertas por email/SMS automáticas**
- ✨ **Dashboard móvil responsive**
- ✨ **Machine Learning drift detection**
- ✨ **Comparación A/B de modelos**
- ✨ **Reportes automáticos PDF**

### Mejoras Técnicas
- 🔧 **Conexión a base de datos**
- 🔧 **Caché distribuido para escalabilidad**
- 🔧 **Autenticación y roles de usuario**
- 🔧 **Logs centralizados**

---

## 💡 Best Practices

### Para Analistas
1. **Revisar alertas diariamente** en Tab 3
2. **Ajustar threshold mensualmente** según feedback
3. **Procesar lotes nocturnos** para análisis completo
4. **Documentar casos especiales** para mejora del modelo

### Para Administradores
1. **Monitorear métricas de performance** semanalmente
2. **Backup de configuraciones** antes de cambios
3. **Test de nuevos thresholds** en modo piloto
4. **Capacitar usuarios** en uso correcto

### Para Desarrolladores
1. **Actualizar modelos** trimestralmente
2. **Monitorear logs de errores** diariamente
3. **Optimizar performance** según volumen
4. **Implementar nuevas features** según feedback

---

## 📞 Soporte y Contacto

### Soporte Técnico
**Ing. Daniel Varela Perez**
- 📧 **Email**: bedaniele0@gmail.com
- 📱 **Teléfono**: +52 55 4189 3428
- 💼 **LinkedIn**: [Perfil Profesional]

### Horarios de Soporte
- **Lunes a Viernes**: 9:00 AM - 6:00 PM (GMT-6)
- **Emergencias**: 24/7 (solo casos críticos)
- **Respuesta promedio**: <4 horas hábiles

### Documentación Adicional
- 📚 **Manual Técnico**: `/docs/technical_manual.pdf`
- 🎥 **Videos Tutorial**: `/docs/video_tutorials/`
- 📖 **API Reference**: `/docs/api_reference.md`

---

**🎉 ¡Dashboard listo para uso en producción!**

*Desarrollado con ❤️ por Ing. Daniel Varela Perez*
