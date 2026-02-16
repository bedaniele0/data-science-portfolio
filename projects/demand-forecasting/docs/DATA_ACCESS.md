# Data Access - Walmart Demand Forecasting

**Autor**: Ing. Daniel Varela Perez  
**Email**: bedaniele0@gmail.com  
**Tel**: +52 55 4189 3428

---

## Overview
Este repositorio **no incluye** el dataset completo M5 por tamaño y licencias. Para reproducir el pipeline completo, descarga el dataset original.

---

## Descarga del Dataset M5 (Kaggle)

1. Crea cuenta y acepta los términos:  
https://www.kaggle.com/competitions/m5-forecasting-accuracy

2. Instala Kaggle CLI y configura credenciales:

```bash
pip install kaggle
mkdir -p ~/.kaggle
cp kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

3. Descarga el dataset y descomprime:

```bash
kaggle competitions download -c m5-forecasting-accuracy -p data/raw
unzip data/raw/m5-forecasting-accuracy.zip -d data/raw
```

---

## Ejecución del pipeline completo

```bash
make process-data
make train
make predict
```

---

## Nota
Para demo local, puedes ejecutar la API y dashboard con los artefactos ya generados en tu entorno local.
