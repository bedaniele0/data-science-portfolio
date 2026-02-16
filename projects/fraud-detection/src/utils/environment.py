"""
Environment Manager - Gestor de Entornos de Ejecución
=====================================================
Módulo para gestionar configuraciones específicas por entorno

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2025-09-24
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any

# Agregar el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent))
from config import ConfigManager


class EnvironmentManager:
    """
    Gestor de configuraciones específicas por entorno

    Desarrollado por: Ing. Daniel Varela Perez
    Email: bedaniele0@gmail.com | Tel: +52 55 4189 3428
    """

    def __init__(self, environment: str = None):
        """
        Inicializa el gestor de entorno

        Args:
            environment: Nombre del entorno (development, testing, production)
        """
        self.environment = environment or os.getenv('ENVIRONMENT', 'development')
        self.config_manager = ConfigManager()
        self.env_config = self._load_environment_config()

    def _load_environment_config(self) -> Dict[str, Any]:
        """Carga configuración específica del entorno"""
        try:
            project_root = Path(__file__).parent.parent.parent
            env_path = project_root / "configs" / "environment.yaml"

            with open(env_path, 'r', encoding='utf-8') as f:
                env_configs = yaml.safe_load(f)

            return env_configs.get(self.environment, {})
        except FileNotFoundError:
            print(f"⚠️  Archivo environment.yaml no encontrado")
            return {}
        except yaml.YAMLError as e:
            print(f"⚠️  Error parsing environment YAML: {e}")
            return {}

    def get_database_config(self) -> Dict[str, Any]:
        """Obtiene configuración de base de datos para el entorno actual"""
        db_config = self.env_config.get('database', {})

        # Usar variables de entorno si están disponibles
        if os.getenv('DB_HOST'):
            db_config['url'] = (
                f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
            )

        return db_config

    def get_ml_config(self) -> Dict[str, Any]:
        """Obtiene configuración de ML para el entorno actual"""
        ml_config = self.env_config.get('ml_config', {})

        # Combinar con configuración base
        base_model_config = self.config_manager.model_config
        return {**base_model_config, **ml_config}

    def get_performance_config(self) -> Dict[str, Any]:
        """Obtiene configuración de performance"""
        perf_config = self.env_config.get('performance', {})

        # Usar variables de entorno si están disponibles
        if os.getenv('MAX_WORKERS'):
            perf_config['n_jobs'] = int(os.getenv('MAX_WORKERS'))

        if os.getenv('MEMORY_LIMIT_GB'):
            perf_config['memory_limit_gb'] = int(os.getenv('MEMORY_LIMIT_GB'))

        return perf_config

    def get_logging_config(self) -> Dict[str, Any]:
        """Obtiene configuración de logging"""
        return {
            'level': self.env_config.get('log_level', 'INFO'),
            'debug': self.env_config.get('debug', False),
            'file': os.getenv('LOG_FILE', 'logs/fraud_detection.log')
        }

    def is_development(self) -> bool:
        """Verifica si estamos en entorno de desarrollo"""
        return self.environment == 'development'

    def is_production(self) -> bool:
        """Verifica si estamos en entorno de producción"""
        return self.environment == 'production'

    def is_testing(self) -> bool:
        """Verifica si estamos en entorno de testing"""
        return self.environment == 'testing'

    def print_environment_summary(self):
        """Imprime resumen de la configuración del entorno"""
        print(f"\n🌍 CONFIGURACIÓN DE ENTORNO: {self.environment.upper()}")
        print(f"{'='*60}")

        # Base de datos
        db_config = self.get_database_config()
        print(f"🗃️  **BASE DE DATOS**:")
        print(f"• URL: {db_config.get('url', 'N/A')}")
        print(f"• Echo SQL: {db_config.get('echo_sql', 'N/A')}")

        # ML Config
        ml_config = self.get_ml_config()
        print(f"\n🤖 **MACHINE LEARNING**:")
        print(f"• Sample data: {ml_config.get('use_sample_data', 'N/A')}")
        print(f"• Sample size: {ml_config.get('sample_size', 'N/A')}")
        print(f"• Cache models: {ml_config.get('model_cache', 'N/A')}")

        # Performance
        perf_config = self.get_performance_config()
        print(f"\n⚡ **PERFORMANCE**:")
        print(f"• N jobs: {perf_config.get('n_jobs', 'N/A')}")
        print(f"• Memory limit: {perf_config.get('memory_limit_gb', 'N/A')} GB")

        # Logging
        log_config = self.get_logging_config()
        print(f"\n📝 **LOGGING**:")
        print(f"• Level: {log_config.get('level', 'N/A')}")
        print(f"• Debug: {log_config.get('debug', 'N/A')}")
        print(f"• File: {log_config.get('file', 'N/A')}")

        # Security (solo producción)
        if self.is_production():
            security = self.env_config.get('security', {})
            print(f"\n🔒 **SECURITY**:")
            print(f"• Encryption: {security.get('enable_encryption', 'N/A')}")
            print(f"• Audit logs: {security.get('audit_logs', 'N/A')}")
            print(f"• Rate limiting: {security.get('rate_limiting', 'N/A')}")

        print(f"{'='*60}")


# Instancia global del gestor de entorno
env_manager = EnvironmentManager()


def get_environment() -> EnvironmentManager:
    """
    Obtiene instancia global del gestor de entorno

    Returns:
        Instancia de EnvironmentManager
    """
    return env_manager


if __name__ == "__main__":
    # Demo del sistema de entornos
    print("🌍 DEMO - SISTEMA DE GESTIÓN DE ENTORNOS")
    print("Desarrollado por: Ing. Daniel Varela Perez")
    print("Email: bedaniele0@gmail.com | Tel: +52 55 4189 3428")

    # Probar diferentes entornos
    for env_name in ['development', 'testing', 'production']:
        env = EnvironmentManager(env_name)
        env.print_environment_summary()
        print()

    print("💡 **USO RECOMENDADO**:")
    print("export ENVIRONMENT=development  # o testing, production")
    print("python tu_script.py")