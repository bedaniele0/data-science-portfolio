#!/usr/bin/env python3
"""
Setup Verification Script - Verificación Completa del Sistema
============================================================
Script completo para verificar que el proyecto está configurado correctamente

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2025-09-24
"""

import sys
import platform
import os
from pathlib import Path


def print_header():
    """Imprime header del script"""
    print("="*60)
    print("🚀 VERIFICACIÓN COMPLETA DEL SISTEMA")
    print("="*60)
    print("📊 Proyecto: Fraud Detection System")
    print("👨‍💻 Autor: Ing. Daniel Varela Perez")
    print("📧 Email: bedaniele0@gmail.com")
    print("📱 Tel: +52 55 4189 3428")
    print("="*60)


def check_system_info():
    """Verifica información del sistema"""
    print("\n🖥️  INFORMACIÓN DEL SISTEMA:")
    print(f"✅ Sistema operativo: {platform.system()} {platform.release()}")
    print(f"✅ Arquitectura: {platform.machine()}")
    print(f"✅ Python version: {sys.version.split()[0]}")
    print(f"✅ Python path: {sys.executable}")


def check_project_structure():
    """Verifica estructura del proyecto"""
    print("\n📁 ESTRUCTURA DEL PROYECTO:")

    required_dirs = [
        "data/raw",
        "data/processed",
        "src/data",
        "src/models",
        "src/utils",
        "src/streaming",
        "notebooks",
        "configs",
        "tests",
        "dashboard"
    ]

    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"⚠️  {dir_path}/ - No encontrado")


def check_config_files():
    """Verifica archivos de configuración"""
    print("\n⚙️  ARCHIVOS DE CONFIGURACIÓN:")

    config_files = [
        "configs/config.yaml",
        "configs/environment.yaml",
        ".env.example",
        ".gitignore",
        "requirements.txt",
        "Makefile",
        "README.md"
    ]

    for file_path in config_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} - No encontrado")


def check_python_environment():
    """Verifica entorno virtual Python"""
    print("\n🐍 ENTORNO VIRTUAL:")

    # Verificar si estamos en un virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"✅ Virtual environment activo: {sys.prefix}")
    else:
        print("⚠️  No se detectó virtual environment activo")

    # Verificar directorio venv
    if Path("venv_fraud").exists():
        print("✅ Directorio venv_fraud/ encontrado")
    else:
        print("❌ Directorio venv_fraud/ no encontrado")


def check_libraries():
    """Verifica librerías instaladas"""
    print("\n📦 LIBRERÍAS PRINCIPALES:")

    libraries = {
        'pandas': 'Análisis de datos',
        'numpy': 'Computación numérica',
        'scikit-learn': 'Machine Learning',
        'xgboost': 'Gradient Boosting',
        'lightgbm': 'Light Gradient Boosting',
        'catboost': 'CatBoost',
        'matplotlib': 'Visualización base',
        'seaborn': 'Visualización estadística',
        'plotly': 'Visualización interactiva',
        'streamlit': 'Dashboard web',
        'shap': 'Explicabilidad ML',
        'imbalanced-learn': 'Balanceado de datos',
        'sqlalchemy': 'ORM base de datos',
        'pyyaml': 'Configuración YAML',
        'python-dotenv': 'Variables de entorno',
        'jupyter': 'Notebooks',
        'pytest': 'Testing framework',
        'black': 'Code formatter'
    }

    installed_count = 0

    for lib_name, description in libraries.items():
        try:
            if lib_name == 'scikit-learn':
                import sklearn
                version = sklearn.__version__
            else:
                lib = __import__(lib_name.replace('-', '_'))
                version = getattr(lib, '__version__', 'N/A')

            print(f"✅ {lib_name:20} v{version:10} - {description}")
            installed_count += 1

        except ImportError:
            print(f"❌ {lib_name:20} {'':10} - {description} (No instalado)")

    print(f"\n📊 Resumen: {installed_count}/{len(libraries)} librerías instaladas")


def check_dataset():
    """Verifica dataset"""
    print("\n💾 DATASET:")

    dataset_path = Path("data/raw/creditcard.csv")

    if not dataset_path.exists():
        print("❌ Dataset no encontrado en data/raw/creditcard.csv")
        return False

    try:
        import pandas as pd

        # Información básica del dataset
        file_size = dataset_path.stat().st_size / (1024 * 1024)  # MB
        print(f"✅ Archivo encontrado: {file_size:.1f} MB")

        # Cargar primeras filas para verificar estructura
        df = pd.read_csv(dataset_path, nrows=100)
        print(f"✅ Estructura verificada: {df.shape[1]} columnas")
        print(f"✅ Columnas: {', '.join(df.columns[:5])}...")

        # Verificar columna objetivo
        if 'Class' in df.columns:
            fraud_rate = df['Class'].mean()
            print(f"✅ Columna objetivo 'Class' encontrada")
            print(f"✅ Tasa de fraude (muestra): {fraud_rate:.3%}")
        else:
            print("⚠️  Columna 'Class' no encontrada")

        return True

    except Exception as e:
        print(f"❌ Error cargando dataset: {e}")
        return False


def check_configuration_system():
    """Verifica sistema de configuración"""
    print("\n🔧 SISTEMA DE CONFIGURACIÓN:")

    try:
        # Verificar que se pueden importar los módulos de configuración
        sys.path.append("src/utils")
        from config import ConfigManager
        from environment import EnvironmentManager

        print("✅ Módulos de configuración importados")

        # Probar ConfigManager
        config = ConfigManager()
        project_name = config.get('project.name')
        print(f"✅ ConfigManager: Proyecto '{project_name}'")

        # Probar EnvironmentManager
        env = EnvironmentManager()
        env_name = env.environment
        print(f"✅ EnvironmentManager: Entorno '{env_name}'")

        # Validar configuración
        is_valid = config.validate_config()
        if is_valid:
            print("✅ Configuración válida")
        else:
            print("⚠️  Configuración con problemas")

        return True

    except Exception as e:
        print(f"❌ Error en sistema de configuración: {e}")
        return False


def check_makefile():
    """Verifica comandos de Makefile"""
    print("\n🛠️  MAKEFILE:")

    if not Path("Makefile").exists():
        print("❌ Makefile no encontrado")
        return False

    try:
        import subprocess

        # Probar make help
        result = subprocess.run(['make', 'help'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ make help - Funciona")
        else:
            print("⚠️  make help - Error")

        return True

    except Exception as e:
        print(f"❌ Error probando Makefile: {e}")
        return False


def generate_summary():
    """Genera resumen final"""
    print("\n" + "="*60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*60)

    # Lista de verificaciones
    checks = [
        ("Sistema", True),  # Siempre pasa si el script corre
        ("Estructura", Path("src").exists()),
        ("Configuración", Path("configs/config.yaml").exists()),
        ("Virtual env", Path("venv_fraud").exists()),
        ("Dataset", Path("data/raw/creditcard.csv").exists()),
        ("README", Path("README.md").exists()),
        ("Makefile", Path("Makefile").exists())
    ]

    passed = sum(1 for _, status in checks if status)
    total = len(checks)

    for check_name, status in checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name}")

    print(f"\n🎯 RESULTADO: {passed}/{total} verificaciones pasadas")

    if passed == total:
        print("🎉 ¡PROYECTO COMPLETAMENTE CONFIGURADO!")
        print("🚀 Listo para desarrollo de ML")
    elif passed >= total * 0.8:
        print("⚠️  Proyecto mayormente configurado - revisar elementos faltantes")
    else:
        print("❌ Configuración incompleta - revisar setup")

    print("\n👨‍💻 Configurado por: Ing. Daniel Varela Perez")
    print("📧 Soporte: bedaniele0@gmail.com | 📱 +52 55 4189 3428")


def main():
    """Función principal"""
    print_header()
    check_system_info()
    check_project_structure()
    check_config_files()
    check_python_environment()
    check_libraries()
    check_dataset()
    check_configuration_system()
    check_makefile()
    generate_summary()


if __name__ == "__main__":
    main()