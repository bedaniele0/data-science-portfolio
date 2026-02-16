#!/usr/bin/env python3
"""
SQL Analysis Execution Script
=============================
Script para ejecutar el análisis SQL de detección de fraude
cuando el notebook presenta problemas de compatibilidad

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2025-09-24
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
import sys
from pathlib import Path
import json

# Configuraciones
warnings.filterwarnings('ignore')
plt.style.use('default')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Crear directorios necesarios
Path('../reports/figures').mkdir(parents=True, exist_ok=True)

def print_header():
    """Imprime header del análisis"""
    print("🔍 ANÁLISIS SQL - DETECCIÓN DE FRAUDE BANCARIO")
    print("=" * 60)
    print(f"📊 Desarrollado por: Ing. Daniel Varela Perez")
    print(f"📧 Email: bedaniele0@gmail.com")
    print(f"📱 Tel: +52 55 4189 3428")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

def load_and_prepare_data():
    """Carga y prepara los datos"""
    print("📊 CARGANDO DATASET...")

    # Cargar datos
    df = pd.read_csv('../data/raw/creditcard.csv')

    print(f"✅ Dataset cargado exitosamente")
    print(f"📏 Dimensiones: {df.shape}")
    print(f"💾 Tamaño en memoria: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

    # Crear conexión SQLite
    print("🗃️ CONFIGURANDO BASE DE DATOS SQLite...")
    conn = sqlite3.connect(':memory:')
    table_name = 'transactions'
    df.to_sql(table_name, conn, index=False, if_exists='replace')

    print(f"✅ Tabla '{table_name}' creada en SQLite")
    print(f"📊 Registros cargados: {len(df):,}")

    return df, conn

def analyze_fraud_distribution(conn):
    """Análisis de distribución de fraudes"""
    print("\n📊 DISTRIBUCIÓN DE FRAUDES:")

    fraud_dist_query = """
    SELECT
        Class,
        COUNT(*) as total_transactions,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions), 4) as percentage,
        CASE
            WHEN Class = 0 THEN 'Normal'
            WHEN Class = 1 THEN 'Fraud'
        END as transaction_type
    FROM transactions
    GROUP BY Class
    ORDER BY Class;
    """

    fraud_distribution = pd.read_sql_query(fraud_dist_query, conn)
    print(fraud_distribution)

    fraud_rate = fraud_distribution[fraud_distribution['Class'] == 1]['percentage'].iloc[0]
    fraud_count = fraud_distribution[fraud_distribution['Class'] == 1]['total_transactions'].iloc[0]

    print(f"\n🎯 TASA DE FRAUDE: {fraud_rate}%")
    print(f"🚨 TOTAL DE FRAUDES: {fraud_count:,}")

    return fraud_distribution, fraud_rate, fraud_count

def analyze_amounts(conn, df):
    """Análisis de montos"""
    print("\n💰 ESTADÍSTICAS DE MONTOS POR TIPO:")

    amount_stats_query = """
    SELECT
        Class,
        CASE
            WHEN Class = 0 THEN 'Normal'
            WHEN Class = 1 THEN 'Fraud'
        END as transaction_type,
        COUNT(*) as count,
        ROUND(AVG(Amount), 2) as avg_amount,
        ROUND(MIN(Amount), 2) as min_amount,
        ROUND(MAX(Amount), 2) as max_amount
    FROM transactions
    GROUP BY Class
    ORDER BY Class;
    """

    amount_stats = pd.read_sql_query(amount_stats_query, conn)
    print(amount_stats)

    # Calcular percentiles usando pandas
    normal_amounts = df[df['Class'] == 0]['Amount']
    fraud_amounts = df[df['Class'] == 1]['Amount']

    print("\n📊 PERCENTILES ADICIONALES:")
    print(f"Normal - Q25: ${normal_amounts.quantile(0.25):.2f}, Mediana: ${normal_amounts.median():.2f}, Q75: ${normal_amounts.quantile(0.75):.2f}")
    print(f"Fraude - Q25: ${fraud_amounts.quantile(0.25):.2f}, Mediana: ${fraud_amounts.median():.2f}, Q75: ${fraud_amounts.quantile(0.75):.2f}")

    return amount_stats, normal_amounts, fraud_amounts

def analyze_temporal_patterns(conn):
    """Análisis temporal"""
    print("\n⏰ ANÁLISIS TEMPORAL:")

    temporal_analysis_query = """
    WITH time_stats AS (
        SELECT
            Class,
            Time,
            Amount,
            ROUND(Time / 3600.0, 2) as hour_from_start,
            CASE
                WHEN Time < 86400 THEN 'Day_1'
                WHEN Time < 172800 THEN 'Day_2'
                ELSE 'Later'
            END as time_bucket
        FROM transactions
    )
    SELECT
        time_bucket,
        Class,
        CASE WHEN Class = 0 THEN 'Normal' ELSE 'Fraud' END as type,
        COUNT(*) as transaction_count,
        ROUND(AVG(Amount), 2) as avg_amount,
        ROUND(AVG(hour_from_start), 2) as avg_hour
    FROM time_stats
    GROUP BY time_bucket, Class
    ORDER BY time_bucket, Class;
    """

    temporal_analysis = pd.read_sql_query(temporal_analysis_query, conn)
    print(temporal_analysis)

    return temporal_analysis

def feature_engineering_analysis(conn):
    """Feature engineering con window functions"""
    print("\n⚡ ANÁLISIS DE VELOCIDAD DE TRANSACCIONES:")

    velocity_query = """
    WITH transaction_velocity AS (
        SELECT
            *,
            COUNT(*) OVER (
                ORDER BY Time
                RANGE BETWEEN 3600 PRECEDING AND CURRENT ROW
            ) as transactions_last_hour,
            COUNT(*) OVER (
                ORDER BY Time
                RANGE BETWEEN 21600 PRECEDING AND CURRENT ROW
            ) as transactions_last_6hours,
            Time - LAG(Time, 1, Time) OVER (ORDER BY Time) as time_since_last
        FROM transactions
        ORDER BY Time
        LIMIT 10000
    )
    SELECT
        Class,
        CASE WHEN Class = 0 THEN 'Normal' ELSE 'Fraud' END as type,
        ROUND(AVG(transactions_last_hour), 2) as avg_velocity_1h,
        ROUND(AVG(transactions_last_6hours), 2) as avg_velocity_6h,
        ROUND(AVG(time_since_last), 2) as avg_time_between,
        COUNT(*) as total_transactions
    FROM transaction_velocity
    GROUP BY Class
    ORDER BY Class;
    """

    try:
        velocity_analysis = pd.read_sql_query(velocity_query, conn)
        print(velocity_analysis)
    except Exception as e:
        print(f"⚠️ Error en análisis de velocidad (SQLite limitaciones): {str(e)[:100]}...")
        print("Continuando con análisis simplificado...")

    # Análisis de frecuencia por rangos
    print("\n💵 ANÁLISIS DE FRECUENCIA POR RANGOS DE MONTO:")

    amount_frequency_query = """
    WITH amount_ranges AS (
        SELECT
            *,
            CASE
                WHEN Amount = 0 THEN 'Zero'
                WHEN Amount > 0 AND Amount <= 10 THEN 'Very_Low (0-10)'
                WHEN Amount > 10 AND Amount <= 50 THEN 'Low (10-50)'
                WHEN Amount > 50 AND Amount <= 100 THEN 'Medium (50-100)'
                WHEN Amount > 100 AND Amount <= 500 THEN 'High (100-500)'
                WHEN Amount > 500 AND Amount <= 1000 THEN 'Very_High (500-1000)'
                ELSE 'Extreme (>1000)'
            END as amount_range
        FROM transactions
    )
    SELECT
        amount_range,
        COUNT(*) as total_frequency,
        SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) as fraud_frequency,
        ROUND(SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fraud_rate_in_range
    FROM amount_ranges
    GROUP BY amount_range
    ORDER BY
        CASE amount_range
            WHEN 'Zero' THEN 1
            WHEN 'Very_Low (0-10)' THEN 2
            WHEN 'Low (10-50)' THEN 3
            WHEN 'Medium (50-100)' THEN 4
            WHEN 'High (100-500)' THEN 5
            WHEN 'Very_High (500-1000)' THEN 6
            WHEN 'Extreme (>1000)' THEN 7
        END;
    """

    amount_frequency = pd.read_sql_query(amount_frequency_query, conn)
    print(amount_frequency)

    return amount_frequency

def create_visualizations(df, normal_amounts, fraud_amounts):
    """Crear visualizaciones"""
    print("\n📊 Creando visualizaciones...")

    # Visualización 1: Distribución de montos
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Análisis de Distribución de Montos - Normal vs Fraude\nDesarrollado por: Ing. Daniel Varela Perez',
                 fontsize=14, fontweight='bold')

    # Histograma comparativo
    axes[0,0].hist(normal_amounts, bins=50, alpha=0.7, label='Normal', color='blue', density=True)
    axes[0,0].hist(fraud_amounts, bins=50, alpha=0.7, label='Fraude', color='red', density=True)
    axes[0,0].set_xlabel('Monto ($)')
    axes[0,0].set_ylabel('Densidad')
    axes[0,0].set_title('Distribución de Montos')
    axes[0,0].legend()

    # Box plot comparativo
    box_data = [normal_amounts, fraud_amounts]
    box_labels = ['Normal', 'Fraude']
    bp = axes[0,1].boxplot(box_data, labels=box_labels, patch_artist=True)
    bp['boxes'][0].set_facecolor('blue')
    bp['boxes'][1].set_facecolor('red')
    axes[0,1].set_ylabel('Monto ($)')
    axes[0,1].set_title('Box Plot de Montos por Clase')

    # Distribución temporal
    df_temp = df.copy()
    df_temp['Hours'] = df_temp['Time'] / 3600
    normal_times = df_temp[df_temp['Class'] == 0]['Hours']
    fraud_times = df_temp[df_temp['Class'] == 1]['Hours']

    axes[1,0].hist(normal_times, bins=100, alpha=0.7, label='Normal', color='blue', density=True)
    axes[1,0].hist(fraud_times, bins=100, alpha=0.7, label='Fraude', color='red', density=True)
    axes[1,0].set_xlabel('Tiempo (Horas desde inicio)')
    axes[1,0].set_ylabel('Densidad')
    axes[1,0].set_title('Distribución Temporal')
    axes[1,0].legend()

    # Correlación con variables principales
    correlation_cols = ['V1', 'V2', 'V3', 'V4', 'V5', 'Amount', 'Class']
    corr_data = df[correlation_cols].corr()
    class_corr = corr_data['Class'].drop('Class').sort_values(key=abs, ascending=False)

    colors = ['red' if x < 0 else 'green' for x in class_corr.values]
    axes[1,1].bar(range(len(class_corr)), class_corr.values, color=colors, alpha=0.7)
    axes[1,1].set_xticks(range(len(class_corr)))
    axes[1,1].set_xticklabels(class_corr.index, rotation=45)
    axes[1,1].set_ylabel('Correlación con Class')
    axes[1,1].set_title('Correlaciones con Fraude')

    plt.tight_layout()
    plt.savefig('../reports/figures/sql_analysis_complete.png', dpi=300, bbox_inches='tight')
    print("✅ Visualización guardada en ../reports/figures/sql_analysis_complete.png")

    return class_corr

def generate_insights(fraud_rate, fraud_count, normal_amounts, fraud_amounts, class_corr):
    """Generar insights principales"""
    print("\n🎯 INSIGHTS CLAVE IDENTIFICADOS")
    print("=" * 60)

    # Calcular métricas clave
    imbalance_ratio = (len(normal_amounts) + len(fraud_amounts)) / len(fraud_amounts)
    normal_avg = normal_amounts.mean()
    fraud_avg = fraud_amounts.mean()

    insights = {
        'dataset_metrics': {
            'fraud_rate': fraud_rate,
            'fraud_count': fraud_count,
            'imbalance_ratio': imbalance_ratio,
            'normal_avg_amount': normal_avg,
            'fraud_avg_amount': fraud_avg
        },
        'key_findings': [
            f"Desbalanceo extremo: {imbalance_ratio:.1f}:1 (Normal:Fraude)",
            f"Tasa de fraude muy baja: {fraud_rate:.4f}%",
            f"Diferencia en montos promedio: ${abs(normal_avg - fraud_avg):.2f}",
            f"Variable más correlacionada: {class_corr.index[0]} ({class_corr.iloc[0]:.4f})"
        ]
    }

    print(f"\n1. 📊 DESBALANCEO EXTREMO:")
    print(f"   • Ratio: {imbalance_ratio:.1f}:1 (Normal:Fraude)")
    print(f"   • Solo {fraud_rate:.4f}% de transacciones son fraude")

    print(f"\n2. 💰 PATRONES DE MONTOS:")
    print(f"   • Monto promedio normal: ${normal_avg:.2f}")
    print(f"   • Monto promedio fraude: ${fraud_avg:.2f}")

    print(f"\n3. 🔗 VARIABLES MÁS PREDICTIVAS:")
    for var, corr in class_corr.head(3).items():
        direction = "positiva" if corr > 0 else "negativa"
        print(f"   • {var}: {abs(corr):.4f} (correlación {direction})")

    print(f"\n🚀 RECOMENDACIONES PARA MODELADO:")
    print("   • Usar técnicas de balanceado (SMOTE, ADASYN)")
    print("   • Priorizar métricas: Precision, Recall, F1-Score, AUC")
    print("   • Algoritmos recomendados: XGBoost, LightGBM, Random Forest")
    print("   • Validación: StratifiedKFold para mantener distribución")

    return insights

def main():
    """Función principal"""
    print_header()

    # Cargar datos
    df, conn = load_and_prepare_data()

    # Análisis básico
    fraud_distribution, fraud_rate, fraud_count = analyze_fraud_distribution(conn)
    amount_stats, normal_amounts, fraud_amounts = analyze_amounts(conn, df)
    temporal_analysis = analyze_temporal_patterns(conn)

    # Feature engineering
    amount_frequency = feature_engineering_analysis(conn)

    # Visualizaciones
    class_corr = create_visualizations(df, normal_amounts, fraud_amounts)

    # Insights
    insights = generate_insights(fraud_rate, fraud_count, normal_amounts, fraud_amounts, class_corr)

    # Guardar resultados
    with open('../reports/sql_eda_results.json', 'w') as f:
        json.dump(insights, f, indent=2)

    print("\n✅ Resultados guardados en ../reports/sql_eda_results.json")
    print("📊 Análisis SQL completado exitosamente")

    # Cerrar conexión
    conn.close()
    print("✅ Conexión SQLite cerrada")

if __name__ == "__main__":
    main()