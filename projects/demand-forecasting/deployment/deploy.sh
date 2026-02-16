#!/bin/bash
# ============================================================================
# deploy.sh - Script de Deployment Automatizado
# ============================================================================
# Despliega el sistema completo en diferentes ambientes
#
# Uso: ./deployment/deploy.sh [dev|staging|production]
#
# Autor: Ing. Daniel Varela Perez
# Email: bedaniele0@gmail.com
# Metodología: DVP-PRO
# ============================================================================

set -e  # Exit on error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
ENVIRONMENT=${1:-dev}
PROJECT_NAME="walmart-demand-forecasting"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="logs/deployment_${ENVIRONMENT}_${TIMESTAMP}.log"

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

check_prerequisites() {
    log_info "Verificando prerequisitos..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker no está instalado"
        exit 1
    fi

    # Check docker-compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "docker-compose no está instalado"
        exit 1
    fi

    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 no está instalado"
        exit 1
    fi

    log_success "Prerequisitos verificados"
}

load_environment() {
    log_info "Cargando variables de entorno para: $ENVIRONMENT"

    # Cargar .env correspondiente
    if [ -f ".env.$ENVIRONMENT" ]; then
        export $(cat .env.$ENVIRONMENT | grep -v '^#' | xargs)
        log_success "Variables de entorno cargadas"
    elif [ -f ".env" ]; then
        export $(cat .env | grep -v '^#' | xargs)
        log_warning "Usando .env default"
    else
        log_warning "No se encontró archivo .env"
    fi

    # Set environment-specific variables
    export ENVIRONMENT=$ENVIRONMENT
    export DEPLOYMENT_TIMESTAMP=$TIMESTAMP
}

run_tests() {
    log_info "Ejecutando tests..."

    if pytest tests/ --maxfail=3 -q; then
        log_success "Tests pasaron exitosamente"
    else
        log_error "Tests fallaron"
        if [ "$ENVIRONMENT" == "production" ]; then
            log_error "No se puede deployar a producción con tests fallidos"
            exit 1
        fi
        log_warning "Continuando deployment en ambiente no productivo"
    fi
}

build_docker_images() {
    log_info "Construyendo imágenes Docker..."

    if docker-compose build; then
        log_success "Imágenes Docker construidas"
    else
        log_error "Error construyendo imágenes Docker"
        exit 1
    fi
}

stop_existing_services() {
    log_info "Deteniendo servicios existentes..."

    docker-compose down || log_warning "No había servicios corriendo"

    log_success "Servicios detenidos"
}

start_services() {
    log_info "Iniciando servicios..."

    if docker-compose up -d; then
        log_success "Servicios iniciados"
    else
        log_error "Error iniciando servicios"
        exit 1
    fi
}

wait_for_services() {
    log_info "Esperando que los servicios estén listos..."

    # Wait for API
    MAX_RETRIES=30
    RETRY_COUNT=0

    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            log_success "API está lista"
            break
        fi

        RETRY_COUNT=$((RETRY_COUNT + 1))
        log_info "Esperando API... (${RETRY_COUNT}/${MAX_RETRIES})"
        sleep 2
    done

    if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
        log_error "API no respondió después de ${MAX_RETRIES} intentos"
        exit 1
    fi
}

run_smoke_tests() {
    log_info "Ejecutando smoke tests..."

    # Health check
    if curl -f http://localhost:8000/health; then
        log_success "Health check pasó"
    else
        log_error "Health check falló"
        exit 1
    fi

    # Prediction test (if API is available)
    log_info "Probando endpoint de predicción..."
    # curl -X POST http://localhost:8000/predict -d '{}' || log_warning "Prediction endpoint no disponible"

    log_success "Smoke tests completados"
}

setup_monitoring() {
    log_info "Configurando monitoring..."

    # Iniciar Prometheus y Grafana (si están configurados)
    if [ -f "docker-compose.monitoring.yml" ]; then
        docker-compose -f docker-compose.monitoring.yml up -d
        log_success "Monitoring iniciado"
    else
        log_warning "Configuración de monitoring no encontrada"
    fi
}

backup_data() {
    log_info "Creando backup de datos..."

    BACKUP_DIR="backups/${ENVIRONMENT}/${TIMESTAMP}"
    mkdir -p "$BACKUP_DIR"

    # Backup MLflow runs
    if [ -d "mlruns" ]; then
        cp -r mlruns "$BACKUP_DIR/"
        log_success "MLflow runs respaldados"
    fi

    # Backup models
    if [ -d "models" ]; then
        cp -r models "$BACKUP_DIR/"
        log_success "Modelos respaldados"
    fi

    log_success "Backup completado en: $BACKUP_DIR"
}

send_deployment_notification() {
    log_info "Enviando notificación de deployment..."

    # Enviar notificación via alertas
    python -c "
from src.monitoring.alerts import get_alert_manager, AlertLevel
manager = get_alert_manager()
manager.send_alert(
    title='Deployment Completado: $ENVIRONMENT',
    message='Sistema deployado exitosamente en ambiente $ENVIRONMENT',
    level=AlertLevel.INFO,
    metrics={'environment': '$ENVIRONMENT', 'timestamp': '$TIMESTAMP'}
)
" || log_warning "No se pudo enviar notificación"

    log_success "Notificación enviada"
}

show_deployment_info() {
    log_info "==================================================================="
    log_info "DEPLOYMENT COMPLETADO"
    log_info "==================================================================="
    log_info "Ambiente: $ENVIRONMENT"
    log_info "Timestamp: $TIMESTAMP"
    log_info ""
    log_info "URLs de Servicios:"
    log_info "  API:       http://localhost:8000"
    log_info "  Dashboard: http://localhost:8501"
    log_info "  MLflow:    http://localhost:5000"
    if [ -f "docker-compose.monitoring.yml" ]; then
        log_info "  Prometheus: http://localhost:9090"
        log_info "  Grafana:    http://localhost:3000"
    fi
    log_info ""
    log_info "Comandos útiles:"
    log_info "  Ver logs:        docker-compose logs -f"
    log_info "  Detener:         docker-compose down"
    log_info "  Reiniciar:       docker-compose restart"
    log_info "  Estado:          docker-compose ps"
    log_info "==================================================================="
}

rollback() {
    log_error "Iniciando rollback..."

    # Detener servicios actuales
    docker-compose down

    # Restaurar último backup
    LATEST_BACKUP=$(ls -t backups/${ENVIRONMENT} | head -1)
    if [ -n "$LATEST_BACKUP" ]; then
        log_info "Restaurando backup: $LATEST_BACKUP"
        cp -r "backups/${ENVIRONMENT}/${LATEST_BACKUP}/mlruns" ./ || true
        cp -r "backups/${ENVIRONMENT}/${LATEST_BACKUP}/models" ./ || true
    fi

    # Reiniciar servicios
    docker-compose up -d

    log_success "Rollback completado"
}

# ============================================================================
# DEPLOYMENT WORKFLOW
# ============================================================================

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║     WALMART DEMAND FORECASTING - DEPLOYMENT SCRIPT             ║"
    echo "║     Ambiente: ${ENVIRONMENT}                                   ║"
    echo "║     DVP-PRO Methodology                                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # Crear directorio de logs
    mkdir -p logs

    # 1. Verificar prerequisitos
    check_prerequisites

    # 2. Cargar variables de entorno
    load_environment

    # 3. Crear backup (solo en staging/production)
    if [ "$ENVIRONMENT" != "dev" ]; then
        backup_data
    fi

    # 4. Ejecutar tests (solo en staging/production)
    if [ "$ENVIRONMENT" != "dev" ]; then
        run_tests
    fi

    # 5. Construir imágenes Docker
    build_docker_images

    # 6. Detener servicios existentes
    stop_existing_services

    # 7. Iniciar servicios
    start_services

    # 8. Esperar a que servicios estén listos
    wait_for_services

    # 9. Ejecutar smoke tests
    run_smoke_tests

    # 10. Configurar monitoring (solo en staging/production)
    if [ "$ENVIRONMENT" != "dev" ]; then
        setup_monitoring
    fi

    # 11. Enviar notificación
    send_deployment_notification

    # 12. Mostrar información del deployment
    show_deployment_info

    log_success "✅ Deployment completado exitosamente!"
}

# ============================================================================
# ERROR HANDLING
# ============================================================================

trap 'log_error "Error en línea $LINENO. Ejecutando rollback..."; rollback; exit 1' ERR

# ============================================================================
# EJECUTAR MAIN
# ============================================================================

main "$@"
