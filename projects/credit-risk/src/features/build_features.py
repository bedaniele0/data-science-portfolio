import os
import yaml
import pandas as pd

def build_features():
    """
    Crea nuevas características y guarda el dataset procesado.
    """
    # Construir ruta al config.yaml de forma robusta
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, '..', '..', 'config', 'config.yaml')

    # Cargar configuración
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Construir rutas de datos de manera robusta
    base_dir = os.path.dirname(os.path.dirname(script_dir))
    raw_data_path = os.path.join(base_dir, config['paths']['raw_data'])
    
    print(f"Cargando datos desde: {raw_data_path}")
    df = pd.read_csv(raw_data_path)
    df_featured = df.copy()

    print("Creando nuevas características...")

    # 1. Utilization ratio (solo mes más reciente)
    df_featured["utilization_1"] = df_featured.apply(
        lambda row: row["BILL_AMT1"] / row["LIMIT_BAL"] if row["LIMIT_BAL"] > 0 else 0,
        axis=1,
    )

    # 2. Payment ratios (6 meses)
    for i in range(1, 7):
        pay_col = f"PAY_AMT{i}"
        bill_col = f"BILL_AMT{i}"
        ratio_col = f"payment_ratio_{i}"
        df_featured[ratio_col] = df_featured.apply(
            lambda row: row[pay_col] / row[bill_col] if row[bill_col] > 0 else 0,
            axis=1,
        )

    # 3. Age bins (one-hot)
    age = df_featured["AGE"]
    df_featured["AGE_bin_26-35"] = ((age >= 26) & (age <= 35)).astype(int)
    df_featured["AGE_bin_36-45"] = ((age >= 36) & (age <= 45)).astype(int)
    df_featured["AGE_bin_46-60"] = ((age >= 46) & (age <= 60)).astype(int)
    df_featured["AGE_bin_60+"] = (age > 60).astype(int)

    # 4. Agrupación de categorías
    df_featured["EDUCATION_grouped"] = df_featured["EDUCATION"].replace({0: 4, 5: 4, 6: 4})
    df_featured["MARRIAGE_grouped"] = df_featured["MARRIAGE"].replace({0: 3})

    print("Características creadas:")
    new_cols = [col for col in df_featured.columns if col not in df.columns]
    print(new_cols)

    # Guardar dataset
    processed_data_dir = os.path.join(base_dir, config['paths']['processed_data'])
    os.makedirs(processed_data_dir, exist_ok=True)
    processed_data_path = os.path.join(processed_data_dir, "featured_dataset.csv")
    dataset_final_path = os.path.join(processed_data_dir, "dataset_final.csv")
    
    df_featured.to_csv(processed_data_path, index=False)
    df_featured.to_csv(dataset_final_path, index=False)
    print(f"\nDataset procesado guardado en: {processed_data_path}")
    print(f"Dataset final guardado en: {dataset_final_path}")
    print(f"Nuevas dimensiones: {df_featured.shape}")

if __name__ == '__main__':
    build_features()
