#!/usr/bin/env python3
"""
Script de Lanzamiento del Dashboard de Detección de Fraudes
==========================================================
Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428

Este script facilita el lanzamiento del dashboard con configuración automática.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    """Ejecutar dashboard de detección de fraudes"""

    print("🚀 Iniciando Dashboard de Detección de Fraudes")
    print("=" * 50)
    print("👨‍💻 Desarrollado por: Ing. Daniel Varela Perez")
    print("📧 Email: bedaniele0@gmail.com")
    print("📱 Tel: +52 55 4189 3428")
    print("=" * 50)

    # Verificar estructura del proyecto
    dashboard_path = Path(__file__).parent / "dashboard" / "fraud_detection_dashboard.py"
    models_path = Path(__file__).parent / "models"

    if not dashboard_path.exists():
        print("❌ Error: No se encuentra el archivo del dashboard")
        print(f"   Ruta esperada: {dashboard_path}")
        return False

    if not models_path.exists():
        print("❌ Error: No se encuentra el directorio de modelos")
        print(f"   Ruta esperada: {models_path}")
        return False

    # Verificar modelos disponibles
    model_files = list(models_path.glob("*.pkl"))
    config_files = list(models_path.glob("*.json"))

    print(f"📁 Modelos encontrados: {len(model_files)}")
    for model_file in model_files:
        print(f"   • {model_file.name}")

    print(f"⚙️ Configuraciones encontradas: {len(config_files)}")
    for config_file in config_files:
        print(f"   • {config_file.name}")

    print("\n🔧 Verificando dependencias...")

    # Verificar dependencias críticas
    try:
        import streamlit
        import pandas
        import plotly
        import joblib
        print("✅ Todas las dependencias están instaladas")
    except ImportError as e:
        print(f"❌ Error: Falta dependencia - {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

    print(f"\n🌐 Lanzando dashboard...")
    print(f"📍 Puerto: 8501")
    print(f"🔗 URL: http://localhost:8501")
    print("\n⏱️ Espera unos segundos para que se abra automáticamente...")

    # Configurar variables de entorno
    env = os.environ.copy()
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'

    try:
        # Cambiar al directorio del dashboard
        os.chdir(dashboard_path.parent)

        # Ejecutar streamlit
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run",
            str(dashboard_path.name),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], env=env)

        # Esperar y abrir navegador
        time.sleep(3)
        webbrowser.open('http://localhost:8501')

        print("\n✅ Dashboard iniciado exitosamente!")
        print("🛑 Para detener: Ctrl+C")
        print("📊 Para recargar: F5 en el navegador")

        # Esperar a que el proceso termine
        process.wait()

    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard detenido por el usuario")
        process.terminate()
        return True
    except Exception as e:
        print(f"\n❌ Error ejecutando dashboard: {e}")
        return False

    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Fallo al iniciar el dashboard")
        print("📝 Pasos para solucionar:")
        print("   1. Verifica que existe el archivo dashboard/fraud_detection_dashboard.py")
        print("   2. Instala dependencias: pip install -r requirements.txt")
        print("   3. Verifica que los modelos estén en la carpeta models/")
        sys.exit(1)
    else:
        print("\n✅ Dashboard ejecutado exitosamente")