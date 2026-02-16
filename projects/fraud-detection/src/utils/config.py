"""
Configuration Manager - Sistema de Gestión de Configuración
==========================================================
Módulo para cargar y gestionar configuraciones del proyecto

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2025-09-24
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """
    Gestor centralizado de configuraciones del proyecto

    Desarrollado por: Ing. Daniel Varela Perez
    Email: bedaniele0@gmail.com | Tel: +52 55 4189 3428
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa el gestor de configuración

        Args:
            config_path: Ruta al archivo de configuración YAML
        """
        if config_path is None:
            # Buscar config.yaml en el directorio configs/
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "configs" / "config.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Carga configuración desde archivo YAML"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML: {e}")

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Obtiene valor de configuración usando notación de punto

        Args:
            key_path: Ruta de la clave (ej: 'data.raw_path')
            default: Valor por defecto si no se encuentra la clave

        Returns:
            Valor de configuración
        """
        keys = key_path.split('.')
        value = self.config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    @property
    def project_info(self) -> Dict[str, str]:
        """Información del proyecto"""
        return self.get('project', {})

    @property
    def data_config(self) -> Dict[str, str]:
        """Configuración de datos"""
        return self.get('data', {})

    @property
    def model_config(self) -> Dict[str, Any]:
        """Configuración del modelo"""
        return self.get('model', {})

    @property
    def metrics_config(self) -> Dict[str, float]:
        """Configuración de métricas objetivo"""
        return self.get('metrics', {})

    @property
    def system_config(self) -> Dict[str, Any]:
        """Configuración del sistema"""
        return self.get('system', {})

    def get_database_url(self) -> str:
        """Obtiene URL de base de datos"""
        return self.get('data.db_engine', 'sqlite:///fraud_detection.db')

    def get_raw_data_path(self) -> Path:
        """Obtiene ruta de datos crudos"""
        raw_path = self.get('data.raw_path', 'data/raw/creditcard.csv')
        return Path(raw_path)

    def get_processed_data_path(self) -> Path:
        """Obtiene ruta de datos procesados"""
        processed_path = self.get('data.processed_path', 'data/processed/')
        return Path(processed_path)

    def get_model_params(self) -> Dict[str, Any]:
        """Obtiene parámetros del modelo"""
        return {
            'test_size': self.get('model.test_size', 0.2),
            'random_state': self.get('model.random_state', 42),
            'n_jobs': self.get('model.n_jobs', -1)
        }

    def get_target_metrics(self) -> Dict[str, float]:
        """Obtiene métricas objetivo"""
        return {
            'precision': self.get('metrics.target_precision', 0.995),
            'recall': self.get('metrics.target_recall', 0.85)
        }

    def validate_config(self) -> bool:
        """
        Valida la configuración del proyecto

        Returns:
            True si la configuración es válida, False en caso contrario
        """
        required_keys = [
            'project.name',
            'project.author',
            'data.raw_path',
            'model.test_size',
            'metrics.target_precision'
        ]

        for key in required_keys:
            if self.get(key) is None:
                print(f"⚠️  Clave requerida faltante: {key}")
                return False

        # Validar que archivo de datos existe
        if not self.get_raw_data_path().exists():
            print(f"⚠️  Archivo de datos no encontrado: {self.get_raw_data_path()}")
            return False

        print("✅ Configuración validada exitosamente")
        return True

    def print_config_summary(self):
        """Imprime resumen de la configuración"""
        print(f"\n📋 CONFIGURACIÓN DEL PROYECTO")
        print(f"{'='*50}")

        # Información del proyecto
        project = self.project_info
        print(f"📊 **Proyecto**: {project.get('name', 'N/A')}")
        print(f"👨‍💻 **Autor**: {project.get('author', 'N/A')}")
        print(f"📧 **Email**: {project.get('email', 'N/A')}")
        print(f"🔢 **Versión**: {project.get('version', 'N/A')}")
        print(f"💻 **Plataforma**: {project.get('platform', 'N/A')}")

        # Configuración de datos
        print(f"\n📊 **DATOS**:")
        print(f"• Raw data: {self.get('data.raw_path', 'N/A')}")
        print(f"• Processed: {self.get('data.processed_path', 'N/A')}")
        print(f"• Database: {self.get('data.db_engine', 'N/A')}")

        # Configuración del modelo
        print(f"\n🤖 **MODELO**:")
        print(f"• Test size: {self.get('model.test_size', 'N/A')}")
        print(f"• Random state: {self.get('model.random_state', 'N/A')}")
        print(f"• N jobs: {self.get('model.n_jobs', 'N/A')}")

        # Métricas objetivo
        print(f"\n🎯 **MÉTRICAS OBJETIVO**:")
        print(f"• Precisión: {self.get('metrics.target_precision', 'N/A')}")
        print(f"• Recall: {self.get('metrics.target_recall', 'N/A')}")

        # Sistema
        print(f"\n💻 **SISTEMA**:")
        print(f"• Max memoria: {self.get('system.max_memory_gb', 'N/A')} GB")
        print(f"{'='*50}")


# Instancia global del gestor de configuración
config = ConfigManager()


def get_config() -> ConfigManager:
    """
    Obtiene instancia global del gestor de configuración

    Returns:
        Instancia de ConfigManager
    """
    return config


if __name__ == "__main__":
    # Demo del sistema de configuración
    print("🔧 DEMO - SISTEMA DE CONFIGURACIÓN")
    print("Desarrollado por: Ing. Daniel Varela Perez")
    print("Email: bedaniele0@gmail.com | Tel: +52 55 4189 3428\n")

    # Cargar y mostrar configuración
    config_manager = get_config()
    config_manager.print_config_summary()

    # Validar configuración
    print(f"\n🔍 **VALIDACIÓN**:")
    is_valid = config_manager.validate_config()

    # Ejemplos de uso
    print(f"\n💡 **EJEMPLOS DE USO**:")
    print(f"• Nombre proyecto: {config_manager.get('project.name')}")
    print(f"• Email autor: {config_manager.get('project.email')}")
    print(f"• Test size: {config_manager.get('model.test_size')}")
    print(f"• Target precision: {config_manager.get('metrics.target_precision')}")