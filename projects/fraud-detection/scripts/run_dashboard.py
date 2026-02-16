#!/usr/bin/env python3
"""
Script de Lanzamiento del Dashboard de Fraude
============================================
Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Teléfono: +52 55 4189 3428
"""

import subprocess
import sys
import os
from pathlib import Path
import importlib

def check_requirements():
    """Verificar dependencias necesarias"""
    print("🔍 Verificando dependencias...")

    required_packages = [
        'streamlit',
        'plotly',
        'pandas',
        'numpy',
        'scikit-learn',
        'joblib'
    ]

    missing_packages = []

    for package in required_packages:
        # Ajuste especial para scikit-learn
        if package == "scikit-learn":
            module = "sklearn"
        else:
            module = package.replace("-", "_")

        try:
            importlib.import_module(module)
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")

    if missing_packages:
        print(f"\n⚠️ PAQUETES FALTANTES: {missing_packages}")
        print("Instala con: pip install " + " ".join(missing_packages))
        return False

    print("✅ Todas las dependencias están disponibles")
    return True

def check_model_files():
    """Verificar archivos del modelo"""
    print("\n📂 Verificando archivos del modelo...")

    model_files = [
        '../models/improved_recall_threshold_model.pkl',
        '../models/threshold_config.json'
    ]

    fallback_files = [
        '../models/simple_fraud_model.pkl'
    ]

    all_missing = True

    for file_path in model_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
            all_missing = False
        else:
            print(f"  ❌ {file_path}")

    if all_missing:
        print("  🔍 Verificando archivos de fallback...")
        for file_path in fallback_files:
            if Path(file_path).exists():
                print(f"  ✅ {file_path} (fallback)")
                all_missing = False
            else:
                print(f"  ❌ {file_path}")

    if all_missing:
        print("\n⚠️ ARCHIVOS DE MODELO NO ENCONTRADOS")
        print("Ejecuta primero:")
        print("  1. notebooks/03_modeling_simple.ipynb")
        print("  2. notebooks/04_improve_recall.ipynb")
        return False

    print("✅ Archivos de modelo encontrados")
    return True

def check_dashboard_file():
    """Verificar archivo del dashboard"""
    print("\n📱 Verificando archivo del dashboard...")

    dashboard_path = Path('../dashboard/fraud_detection_dashboard.py')

    if dashboard_path.exists():
        print(f"  ✅ {dashboard_path}")
        return True
    else:
        print(f"  ❌ {dashboard_path}")
        print("⚠️ Archivo del dashboard no encontrado")
        return False

def launch_dashboard():
    """Lanzar el dashboard"""
    print("\n🚀 LANZANDO DASHBOARD...")
    print("=" * 50)

    dashboard_path = '../dashboard/fraud_detection_dashboard.py'

    try:
        # Comando para lanzar Streamlit
        cmd = [
            sys.executable, '-m', 'streamlit', 'run',
            dashboard_path,
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--server.headless', 'false'
        ]

        print(f"Ejecutando: {' '.join(cmd)}")
        print("\n🌐 Dashboard disponible en: http://localhost:8501")
        print("📱 Para detener el dashboard: Ctrl+C")
        print("=" * 50)

        # Lanzar el proceso
        subprocess.run(cmd)

    except KeyboardInterrupt:
        print("\n🚩 Dashboard detenido por el usuario")
    except Exception as e:
        print(f"❌ Error lanzando dashboard: {e}")
        print("\n🔧 Solución manual:")
        print(f"streamlit run {dashboard_path}")

def main():
    """Función principal"""
    print("💳 LAUNCHER - DASHBOARD DE DETECCIÓN DE FRAUDE")
    print("=" * 60)
    print("Desarrollado por: Ing. Daniel Varela Perez")
    print("Email: bedaniele0@gmail.com")
    print("Teléfono: +52 55 4189 3428")
    print("=" * 60)

    # Verificaciones previas
    if not check_requirements():
        print("\n❌ Faltan dependencias. Instala los paquetes requeridos.")
        return False

    if not check_model_files():
        print("\n❌ Faltan archivos de modelo. Ejecuta los notebooks de entrenamiento.")
        return False

    if not check_dashboard_file():
        print("\n❌ Archivo del dashboard no encontrado.")
        return False

    # Todo listo, lanzar dashboard
    print("\n✅ TODOS LOS REQUISITOS CUMPLIDOS")
    print("🎯 Lanzando dashboard...")

    try:
        launch_dashboard()
        return True
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        return False

if __name__ == "__main__":
    success = main()

    if not success:
        print(f"\n{'='*60}")
        print("❌ ERROR EN EL LANZAMIENTO")
        print("🔧 Soluciones:")
        print("1. Verifica las dependencias: pip install -r requirements.txt")
        print("2. Ejecuta los notebooks de entrenamiento")
        print("3. Verifica la estructura de directorios")
        print(f"{'='*60}")
        sys.exit(1)
    else:
        print(f"\n{'='*60}")
        print("✅ DASHBOARD EJECUTADO EXITOSAMENTE")
        print(f"{'='*60}")