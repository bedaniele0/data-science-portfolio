#!/usr/bin/env python3
"""
Batch Simulator - Simulador de Procesamiento en Tiempo Real
==========================================================
Simula el procesamiento de transacciones en tiempo real usando batches
para pruebas del pipeline ETL de detección de fraude

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2025-09-24
"""

import pandas as pd
import dask.dataframe as dd
import numpy as np
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
import json
import pickle
from typing import Generator, Dict, List, Tuple, Optional
import logging
import sys
import os

# Agregar paths para imports
sys.path.append(str(Path(__file__).parent.parent / 'utils'))

class BatchSimulator:
    """
    Simulador de procesamiento en batches para detección de fraude

    Simula un entorno de streaming procesando el dataset en batches
    pequeños que llegan secuencialmente
    """

    def __init__(self,
                 data_path: str,
                 batch_size: int = 1000,
                 delay_seconds: float = 1.0,
                 random_delays: bool = True,
                 fraud_boost_factor: float = 2.0):
        """
        Inicializa el simulador de batches

        Args:
            data_path: Ruta al dataset original
            batch_size: Tamaño de batch por iteración
            delay_seconds: Delay base entre batches
            random_delays: Si aplicar delays aleatorios
            fraud_boost_factor: Factor para aumentar fraudes en ciertos batches
        """
        self.data_path = data_path
        self.batch_size = batch_size
        self.delay_seconds = delay_seconds
        self.random_delays = random_delays
        self.fraud_boost_factor = fraud_boost_factor

        # Configurar logging
        self.setup_logging()

        # Cargar y preparar datos
        self.df = None
        self.current_batch = 0
        self.total_batches = 0
        self.processed_transactions = 0
        self.processed_frauds = 0

        # Estadísticas de performance
        self.batch_processing_times = []
        self.simulation_start_time = None

        # Cargar pipeline si existe
        self.scaler = None
        self.feature_columns = None
        self.load_pipeline_components()

        self.logger.info(f"BatchSimulator inicializado")
        self.logger.info(f"Dataset: {data_path}")
        self.logger.info(f"Batch size: {batch_size}")
        self.logger.info(f"Delay: {delay_seconds}s")

    def setup_logging(self):
        """Configura logging para el simulador"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(f'logs/batch_simulator_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
            ]
        )
        self.logger = logging.getLogger('BatchSimulator')

        # Crear directorio de logs si no existe
        Path('logs').mkdir(exist_ok=True)

    def load_pipeline_components(self):
        """Carga componentes del pipeline si están disponibles"""
        try:
            # Intentar cargar scaler
            scaler_path = Path('../../data/processed/scaler.pkl')
            if scaler_path.exists():
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                self.logger.info("Scaler cargado exitosamente")

            # Intentar cargar metadatos
            metadata_path = Path('../../data/processed/pipeline_metadata.json')
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    self.feature_columns = metadata['feature_info']['feature_columns']
                self.logger.info(f"Metadatos cargados - {len(self.feature_columns)} features")

        except Exception as e:
            self.logger.warning(f"No se pudieron cargar componentes del pipeline: {e}")

    def load_data(self):
        """Carga y prepara el dataset para simulación"""
        self.logger.info("Cargando dataset...")

        try:
            self.df = pd.read_csv(self.data_path)
            self.logger.info(f"Dataset cargado: {len(self.df):,} transacciones")

            # Ordenar por tiempo para simulación realista
            self.df = self.df.sort_values('Time').reset_index(drop=True)

            # Calcular batches
            self.total_batches = (len(self.df) - 1) // self.batch_size + 1
            self.logger.info(f"Total batches a procesar: {self.total_batches}")

            # Estadísticas iniciales
            fraud_count = self.df['Class'].sum()
            fraud_rate = fraud_count / len(self.df) * 100
            self.logger.info(f"Fraudes en dataset: {fraud_count:,} ({fraud_rate:.4f}%)")

            return True

        except Exception as e:
            self.logger.error(f"Error cargando dataset: {e}")
            return False

    def create_enhanced_batch(self, batch_df: pd.DataFrame) -> pd.DataFrame:
        """
        Crea un batch enriquecido con feature engineering simulando pipeline real

        Args:
            batch_df: Batch original de datos

        Returns:
            pd.DataFrame: Batch con features adicionales
        """
        batch_enhanced = batch_df.copy()

        try:
            # Feature engineering básico (simulando pipeline completo)

            # Features temporales
            batch_enhanced['hour_from_start'] = batch_enhanced['Time'] / 3600
            batch_enhanced['day_from_start'] = batch_enhanced['Time'] / 86400

            # Features de monto
            batch_enhanced['amount_zscore_global'] = (
                batch_enhanced['Amount'] - batch_enhanced['Amount'].mean()
            ) / (batch_enhanced['Amount'].std() + 1e-8)

            batch_enhanced['amount_percentile'] = batch_enhanced['Amount'].rank(pct=True)
            batch_enhanced['is_zero_amount'] = (batch_enhanced['Amount'] == 0).astype(int)
            batch_enhanced['is_high_amount'] = (batch_enhanced['Amount'] > 1000).astype(int)

            # Features de anomalías
            batch_enhanced['is_extreme_high'] = (batch_enhanced['amount_zscore_global'] > 3).astype(int)
            batch_enhanced['is_extreme_low'] = (batch_enhanced['amount_zscore_global'] < -3).astype(int)

            # Interacciones básicas entre variables V (primeras 5)
            v_cols = [col for col in batch_enhanced.columns if col.startswith('V') and col[1:].isdigit()][:5]
            if len(v_cols) >= 2:
                batch_enhanced['V1_x_V2'] = batch_enhanced.get('V1', 0) * batch_enhanced.get('V2', 0)
                batch_enhanced['V_sum_first5'] = batch_enhanced[v_cols].sum(axis=1)
                batch_enhanced['V_mean_first5'] = batch_enhanced[v_cols].mean(axis=1)

            # Features de velocidad (aproximados dentro del batch)
            batch_enhanced['time_since_last'] = batch_enhanced['Time'].diff().fillna(0)
            batch_enhanced['transactions_in_hour'] = batch_enhanced.groupby(
                batch_enhanced['hour_from_start'].astype(int)
            ).transform('count')['Amount']

            # Agregar timestamp de procesamiento
            batch_enhanced['processing_timestamp'] = datetime.now().isoformat()
            batch_enhanced['batch_id'] = self.current_batch

            return batch_enhanced

        except Exception as e:
            self.logger.error(f"Error en feature engineering del batch: {e}")
            return batch_df

    def simulate_real_time_variations(self, batch_df: pd.DataFrame) -> pd.DataFrame:
        """
        Simula variaciones que podrían ocurrir en tiempo real

        Args:
            batch_df: Batch de datos

        Returns:
            pd.DataFrame: Batch con variaciones simuladas
        """
        batch_varied = batch_df.copy()

        try:
            # Simular datos faltantes ocasionales (1% de probabilidad)
            if random.random() < 0.01:
                missing_cols = random.sample([col for col in batch_varied.columns
                                            if col.startswith('V')], k=min(2, len([col for col in batch_varied.columns if col.startswith('V')])))
                for col in missing_cols:
                    mask = np.random.random(len(batch_varied)) < 0.05  # 5% de missing
                    batch_varied.loc[mask, col] = np.nan

                self.logger.warning(f"Simulando datos faltantes en {missing_cols}")

            # Simular latencia de red (afecta timestamp)
            if self.random_delays:
                network_latency = random.uniform(0.1, 2.0)  # 0.1 a 2 segundos
                time.sleep(network_latency)

            # Simular duplicados ocasionales (muy raro, 0.1%)
            if random.random() < 0.001:
                duplicate_count = random.randint(1, 3)
                duplicates = batch_varied.sample(n=min(duplicate_count, len(batch_varied)))
                batch_varied = pd.concat([batch_varied, duplicates], ignore_index=True)
                self.logger.warning(f"Simulando {duplicate_count} transacciones duplicadas")

            return batch_varied

        except Exception as e:
            self.logger.error(f"Error simulando variaciones: {e}")
            return batch_df

    def process_batch(self, batch_df: pd.DataFrame) -> Dict:
        """
        Procesa un batch de transacciones

        Args:
            batch_df: Batch de datos a procesar

        Returns:
            Dict: Resultados del procesamiento
        """
        batch_start_time = time.time()

        try:
            # Enriquecer batch con feature engineering
            batch_enhanced = self.create_enhanced_batch(batch_df)

            # Simular variaciones de tiempo real
            batch_final = self.simulate_real_time_variations(batch_enhanced)

            # Estadísticas del batch
            fraud_count = batch_final['Class'].sum()
            normal_count = len(batch_final) - fraud_count
            fraud_rate = fraud_count / len(batch_final) * 100 if len(batch_final) > 0 else 0

            # Detectar anomalías simuladas
            high_value_txns = (batch_final['Amount'] > 1000).sum()
            zero_amount_txns = (batch_final['Amount'] == 0).sum()
            extreme_values = (abs(batch_final.get('amount_zscore_global', 0)) > 3).sum()

            # Aplicar normalización si está disponible
            normalized_features = None
            if self.scaler and self.feature_columns:
                try:
                    available_features = [col for col in self.feature_columns if col in batch_final.columns]
                    if available_features:
                        normalized_features = self.scaler.transform(batch_final[available_features])
                except Exception as e:
                    self.logger.warning(f"Error aplicando normalización: {e}")

            # Calcular tiempo de procesamiento
            processing_time = time.time() - batch_start_time
            self.batch_processing_times.append(processing_time)

            # Actualizar estadísticas globales
            self.processed_transactions += len(batch_final)
            self.processed_frauds += fraud_count

            # Resultados del batch
            results = {
                'batch_id': self.current_batch,
                'timestamp': datetime.now().isoformat(),
                'transactions_processed': len(batch_final),
                'fraud_count': fraud_count,
                'normal_count': normal_count,
                'fraud_rate_percent': fraud_rate,
                'processing_time_seconds': processing_time,
                'features_created': len(batch_enhanced.columns) - len(batch_df.columns),
                'anomalies_detected': {
                    'high_value': high_value_txns,
                    'zero_amount': zero_amount_txns,
                    'extreme_values': extreme_values
                },
                'data_quality': {
                    'missing_values': batch_final.isnull().sum().sum(),
                    'duplicates': len(batch_final) - len(batch_final.drop_duplicates())
                }
            }

            return results

        except Exception as e:
            self.logger.error(f"Error procesando batch {self.current_batch}: {e}")
            return {
                'batch_id': self.current_batch,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def run_simulation(self, max_batches: Optional[int] = None) -> Generator[Dict, None, None]:
        """
        Ejecuta la simulación de procesamiento en batches

        Args:
            max_batches: Número máximo de batches a procesar (None para todos)

        Yields:
            Dict: Resultados de cada batch procesado
        """
        if self.df is None:
            if not self.load_data():
                return

        self.simulation_start_time = time.time()
        self.current_batch = 0

        self.logger.info("Iniciando simulación de batches...")

        batches_to_process = min(max_batches or float('inf'), self.total_batches)

        try:
            for batch_idx in range(int(batches_to_process)):
                self.current_batch = batch_idx + 1

                # Obtener batch actual
                start_idx = batch_idx * self.batch_size
                end_idx = min(start_idx + self.batch_size, len(self.df))
                batch_df = self.df.iloc[start_idx:end_idx].copy()

                # Procesar batch
                batch_results = self.process_batch(batch_df)

                # Log de progreso
                if batch_idx % 10 == 0:  # Log cada 10 batches
                    progress = (batch_idx + 1) / batches_to_process * 100
                    avg_processing_time = np.mean(self.batch_processing_times[-10:])
                    self.logger.info(
                        f"Progreso: {progress:.1f}% "
                        f"(Batch {batch_idx + 1}/{batches_to_process}) - "
                        f"Tiempo promedio: {avg_processing_time:.3f}s"
                    )

                yield batch_results

                # Aplicar delay entre batches
                if self.delay_seconds > 0:
                    if self.random_delays:
                        actual_delay = self.delay_seconds * random.uniform(0.5, 1.5)
                    else:
                        actual_delay = self.delay_seconds
                    time.sleep(actual_delay)

        except KeyboardInterrupt:
            self.logger.info("Simulación interrumpida por el usuario")
        except Exception as e:
            self.logger.error(f"Error en simulación: {e}")
        finally:
            self.generate_final_report()

    def generate_final_report(self):
        """Genera reporte final de la simulación"""
        if self.simulation_start_time is None:
            return

        total_time = time.time() - self.simulation_start_time

        self.logger.info("=" * 60)
        self.logger.info("REPORTE FINAL DE SIMULACIÓN")
        self.logger.info("=" * 60)
        self.logger.info(f"Batches procesados: {self.current_batch}")
        self.logger.info(f"Transacciones procesadas: {self.processed_transactions:,}")
        self.logger.info(f"Fraudes detectados: {self.processed_frauds:,}")

        if self.processed_transactions > 0:
            overall_fraud_rate = self.processed_frauds / self.processed_transactions * 100
            self.logger.info(f"Tasa de fraude global: {overall_fraud_rate:.4f}%")

        self.logger.info(f"Tiempo total: {total_time:.2f}s ({total_time/60:.2f} min)")

        if self.batch_processing_times:
            avg_processing_time = np.mean(self.batch_processing_times)
            throughput = self.processed_transactions / total_time
            self.logger.info(f"Tiempo promedio por batch: {avg_processing_time:.3f}s")
            self.logger.info(f"Throughput: {throughput:.1f} transacciones/segundo")

        self.logger.info("=" * 60)

def main():
    """Función principal para ejecutar el simulador"""
    print("🔄 BATCH SIMULATOR - DETECCIÓN DE FRAUDE")
    print("=" * 60)
    print("📊 Desarrollado por: Ing. Daniel Varela Perez")
    print("📧 Email: bedaniele0@gmail.com")
    print("📱 Tel: +52 55 4189 3428")
    print("=" * 60)

    # Configuración del simulador
    data_path = '../../data/raw/creditcard.csv'

    # Verificar que existe el archivo
    if not Path(data_path).exists():
        print(f"❌ Error: No se encuentra el dataset en {data_path}")
        return

    # Crear simulador
    simulator = BatchSimulator(
        data_path=data_path,
        batch_size=500,  # Batches más pequeños para simulación realista
        delay_seconds=0.5,  # Delay más corto para demo
        random_delays=True,
        fraud_boost_factor=1.5
    )

    print(f"✅ Simulador inicializado")
    print(f"🎯 Ejecutando simulación con batches de 500 transacciones...")

    # Ejecutar simulación (máximo 20 batches para demo)
    batch_count = 0
    fraud_alerts = 0

    try:
        for result in simulator.run_simulation(max_batches=20):
            batch_count += 1

            if 'error' in result:
                print(f"❌ Error en batch {result['batch_id']}: {result['error']}")
                continue

            # Mostrar resultados del batch
            fraud_rate = result['fraud_rate_percent']
            processing_time = result['processing_time_seconds']

            print(f"📊 Batch {result['batch_id']:2d}: "
                  f"{result['transactions_processed']:3d} txns, "
                  f"{result['fraud_count']:2d} fraudes ({fraud_rate:5.2f}%), "
                  f"{processing_time:.3f}s")

            # Alertas de fraude alto
            if fraud_rate > 1.0:  # Más del 1% de fraude
                fraud_alerts += 1
                print(f"🚨 ALERTA: Alta tasa de fraude detectada ({fraud_rate:.2f}%)")

    except KeyboardInterrupt:
        print(f"\n⏹️ Simulación detenida por el usuario")

    print(f"\n✅ Simulación completada")
    print(f"📊 Batches procesados: {batch_count}")
    print(f"🚨 Alertas de fraude: {fraud_alerts}")
    print(f"👨‍💻 Desarrollado por: Ing. Daniel Varela Perez")

if __name__ == "__main__":
    main()