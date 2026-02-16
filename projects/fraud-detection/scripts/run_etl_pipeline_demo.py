#!/usr/bin/env python3
"""
Demo del Pipeline ETL con Dask
==============================
Script demo para ejecutar el pipeline ETL distribuido
con una muestra del dataset para verificar funcionamiento

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2025-09-24
"""

import dask
import dask.dataframe as dd
from dask.distributed import Client
from dask.diagnostics import ProgressBar
import pandas as pd
import numpy as np
from datetime import datetime
import time
from pathlib import Path
import warnings

# Configuración
warnings.filterwarnings('ignore')
dask.config.set({'dataframe.query-planning': False})

def setup_demo_client():
    """Configura cliente Dask para demo"""
    print("🔧 CONFIGURANDO CLIENTE DASK PARA DEMO...")

    client = Client(
        n_workers=2,
        threads_per_worker=2,
        memory_limit='2GB',
        processes=True,
        silence_logs=False
    )

    print(f"✅ Cliente configurado: {client.dashboard_link}")
    return client

def load_sample_data(sample_size=10000):
    """Carga muestra del dataset para demo"""
    print(f"📊 CARGANDO MUESTRA DEL DATASET ({sample_size:,} registros)...")

    data_path = 'data/raw/creditcard.csv'

    # Cargar muestra
    df = pd.read_csv(data_path, nrows=sample_size)
    print(f"✅ Muestra cargada: {len(df):,} registros, {df['Class'].sum()} fraudes")

    return df

def create_dask_sample(df, chunk_size=2000):
    """Convierte muestra a DataFrame de Dask"""
    print(f"🔄 CONVIRTIENDO A DASK DATAFRAME...")

    # Crear DataFrame de Dask
    ddf = dd.from_pandas(df, npartitions=max(1, len(df) // chunk_size))

    print(f"✅ Dask DataFrame: {ddf.npartitions} particiones")
    return ddf

def demo_feature_engineering(ddf):
    """Demo de feature engineering distribuido"""
    print(f"⚡ DEMO - FEATURE ENGINEERING DISTRIBUIDO...")

    def add_demo_features(partition):
        """Añade features demo a cada partición"""
        # Features temporales
        partition['hour_from_start'] = partition['Time'] / 3600
        partition['day_from_start'] = partition['Time'] / 86400

        # Features de monto
        partition['amount_log'] = np.log1p(partition['Amount'])
        partition['is_zero_amount'] = (partition['Amount'] == 0).astype(int)
        partition['is_high_amount'] = (partition['Amount'] > 1000).astype(int)

        # Z-score simplificado
        amount_mean = partition['Amount'].mean()
        amount_std = partition['Amount'].std()
        if amount_std > 0:
            partition['amount_zscore'] = (partition['Amount'] - amount_mean) / amount_std
        else:
            partition['amount_zscore'] = 0

        # Interacción V1 * V2 (si existen)
        if 'V1' in partition.columns and 'V2' in partition.columns:
            partition['V1_x_V2'] = partition['V1'] * partition['V2']

        return partition

    # Aplicar feature engineering
    with ProgressBar():
        ddf_enhanced = ddf.map_partitions(add_demo_features)

        # Computar para verificar
        sample_result = ddf_enhanced.head(5)

    new_features = [col for col in sample_result.columns if col not in ddf.columns]
    print(f"✅ Features creados: {new_features}")

    return ddf_enhanced

def demo_temporal_split(ddf, train_ratio=0.7):
    """Demo de split temporal"""
    print(f"📅 DEMO - SPLIT TEMPORAL...")

    with ProgressBar():
        # Obtener estadísticas temporales
        time_min = ddf['Time'].min().compute()
        time_max = ddf['Time'].max().compute()

        # Calcular punto de corte
        time_range = time_max - time_min
        train_cutoff = time_min + (time_range * train_ratio)

        # Crear splits
        train_ddf = ddf[ddf['Time'] < train_cutoff]
        test_ddf = ddf[ddf['Time'] >= train_cutoff]

        # Obtener tamaños
        train_size = len(train_ddf)
        test_size = len(test_ddf)

        train_fraud = train_ddf['Class'].sum().compute()
        test_fraud = test_ddf['Class'].sum().compute()

    print(f"✅ Train: {train_size:,} registros, {train_fraud} fraudes")
    print(f"✅ Test: {test_size:,} registros, {test_fraud} fraudes")

    return train_ddf, test_ddf

def demo_save_parquet(ddf, output_path):
    """Demo de guardado en Parquet"""
    print(f"💾 DEMO - GUARDANDO EN PARQUET...")
    print(f"• Ruta: {output_path}")

    start_time = time.time()

    try:
        with ProgressBar():
            ddf.to_parquet(output_path, write_index=False, compression='snappy')

        save_time = time.time() - start_time

        # Verificar archivo guardado
        if Path(output_path).exists():
            # Calcular tamaño
            total_size = sum(f.stat().st_size for f in Path(output_path).rglob('*.parquet'))
            print(f"✅ Guardado exitoso: {total_size / (1024**2):.1f} MB en {save_time:.2f}s")

            # Verificar carga
            ddf_loaded = dd.read_parquet(output_path)
            print(f"✅ Verificación: {ddf_loaded.npartitions} particiones cargadas")

            return True
        else:
            print(f"❌ Error: archivo no encontrado")
            return False

    except Exception as e:
        print(f"❌ Error guardando: {e}")
        return False

def main():
    """Función principal del demo"""
    print("🚀 DEMO - PIPELINE ETL DISTRIBUIDO CON DASK")
    print("=" * 60)
    print("📊 Desarrollado por: Ing. Daniel Varela Perez")
    print("📧 Email: bedaniele0@gmail.com")
    print("📱 Tel: +52 55 4189 3428")
    print("📅 Fecha: 2025-09-24")
    print("=" * 60)

    # Crear directorios necesarios
    Path('data/processed/demo').mkdir(parents=True, exist_ok=True)

    try:
        # 1. Configurar Dask
        client = setup_demo_client()

        # 2. Cargar muestra de datos
        df_sample = load_sample_data(sample_size=5000)  # Muestra pequeña para demo

        # 3. Convertir a Dask
        ddf = create_dask_sample(df_sample, chunk_size=1000)

        # 4. Feature engineering
        ddf_enhanced = demo_feature_engineering(ddf)

        # 5. Split temporal
        train_ddf, test_ddf = demo_temporal_split(ddf_enhanced)

        # 6. Guardar resultados
        print(f"\\n💾 GUARDANDO RESULTADOS DEL DEMO...")

        train_saved = demo_save_parquet(train_ddf, 'data/processed/demo/train_demo.parquet')
        test_saved = demo_save_parquet(test_ddf, 'data/processed/demo/test_demo.parquet')

        # 7. Resumen final
        print(f"\\n🎯 RESUMEN DEL DEMO")
        print(f"{'='*40}")

        if train_saved and test_saved:
            print(f"✅ Pipeline ejecutado exitosamente")
            print(f"📁 Archivos generados:")
            print(f"  • train_demo.parquet")
            print(f"  • test_demo.parquet")

            # Estadísticas finales
            with ProgressBar():
                train_stats = train_ddf.describe().compute()

            print(f"\\n📊 ESTADÍSTICAS TRAIN SET:")
            print(f"• Registros: {len(train_ddf):,}")
            print(f"• Features: {len(train_ddf.columns)}")
            print(f"• Monto promedio: ${train_stats.loc['mean', 'Amount']:.2f}")

            print(f"\\n✅ DEMO COMPLETADO EXITOSAMENTE")
            print(f"🎉 Pipeline ETL distribuido funciona correctamente")

        else:
            print(f"❌ Algunos componentes fallaron")

    except Exception as e:
        print(f"❌ Error en demo: {e}")

    finally:
        # Cerrar cliente Dask
        try:
            client.close()
            print(f"🔧 Cliente Dask cerrado")
        except:
            pass

    print(f"\\n👨‍💻 Demo desarrollado por: Ing. Daniel Varela Perez")
    print(f"📧 bedaniele0@gmail.com | 📱 +52 55 4189 3428")

if __name__ == "__main__":
    main()