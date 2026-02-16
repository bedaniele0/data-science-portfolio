# Docker Troubleshooting Guide

**Author**: Ing. Daniel Varela Perez
**Date**: December 5, 2024

---

## 🚨 Error: "no such host" al hacer docker-compose up

### Síntoma
```
failed to do request: Head "https://registry-1.docker.io/...":
dial tcp: lookup registry-1.docker.io: no such host
```

### Causa
Docker no puede conectarse al registro de Docker Hub por:
1. Problema de conexión a internet
2. Docker Desktop no completamente iniciado
3. Configuración de DNS/proxy
4. Firewall bloqueando conexión

---

## ✅ Soluciones

### Solución 1: Reiniciar Docker Desktop

1. **Cerrar Docker Desktop completamente**
   - Click en ícono de Docker en barra de menú
   - Quit Docker Desktop

2. **Esperar 10 segundos**

3. **Abrir Docker Desktop de nuevo**

4. **Esperar a que diga "Docker Desktop is running"**
   - Debería aparecer ballena verde en barra de menú

5. **Intentar de nuevo**:
   ```bash
   docker-compose up -d --build
   ```

---

### Solución 2: Verificar Conexión a Internet

```bash
# Probar conectividad
ping -c 3 registry-1.docker.io
```

**Si falla**: Verificar conexión WiFi/Ethernet

---

### Solución 3: Configurar DNS en Docker

1. Abrir Docker Desktop
2. Settings → Docker Engine
3. Agregar configuración DNS:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```
4. Apply & Restart

---

### Solución 4: Usar API Sin Docker ⭐ **ALTERNATIVA**

Si Docker sigue dando problemas, puedes correr el API localmente:

```bash
# Opción A: Script automatizado
./run_api_local.sh

# Opción B: Manual
source venv/bin/activate
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

---

## 🔍 Verificar Estado de Docker

### Comprobar que Docker está corriendo:
```bash
docker info
```

**Output esperado**: Información del sistema Docker

**Si error**: Docker Desktop no está corriendo

---

### Comprobar conectividad a Docker Hub:
```bash
docker pull hello-world
```

**Si funciona**: Conexión OK, problema es otro
**Si falla**: Problema de red/proxy

---

## 📊 Comparación: Docker vs Local

| Aspecto | Docker | Local |
|---------|--------|-------|
| **Setup** | Más complejo | Más simple |
| **Isolation** | Total | Compartido |
| **Portability** | Alta | Baja |
| **Performance** | Overhead mínimo | Nativo |
| **Troubleshooting** | Más difícil | Más fácil |

**Para desarrollo local**: Usar `./run_api_local.sh`
**Para producción**: Docker es obligatorio

---

## 🎯 Siguiente Paso Recomendado

Dado el problema de Docker, te recomiendo:

### **Opción A: API Local** ⭐ **MÁS RÁPIDO**

```bash
# 1. Correr API localmente
./run_api_local.sh

# 2. En otra terminal, probar
./test_api.sh
```

**Ventajas**:
- ✅ No depende de Docker
- ✅ Más rápido de iniciar
- ✅ Más fácil de debuggear
- ✅ Misma funcionalidad

**Desventajas**:
- ⚠️ No valida Docker deployment
- ⚠️ Depende de ambiente local

---

### **Opción B: Fix Docker**

1. Restart Docker Desktop
2. Verificar conexión
3. Configurar DNS
4. Reintentar build

**Tiempo**: 10-15 minutos
**Éxito**: Variable

---

## 💡 Recomendación

**Para continuar con validación**:
→ Usa `./run_api_local.sh` (más rápido)

**Para validar Docker**:
→ Fix Docker más tarde cuando tengas tiempo

**No bloquea desarrollo**: API funciona igual localmente

---

## 📞 Soporte

Si problemas persisten:

**Author**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com

---
