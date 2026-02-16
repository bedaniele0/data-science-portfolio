# 🚀 Installation Guide - Walmart Demand Forecasting

**Autor**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428

---

## Prerequisites

- **Python**: 3.10 or higher
- **pip**: Latest version
- **Git**: For version control
- **Jupyter**: For notebooks (optional)

---

## Step 1: Clone the Repository

```bash
cd /Users/danielevarella/Desktop
cd walmart-demand-forecasting
```

---

## Step 2: Create Virtual Environment

### Option A: Using venv (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify activation
which python  # Should show path to venv/bin/python
```

### Option B: Using conda

```bash
# Create conda environment
conda create -n walmart-forecast python=3.10

# Activate
conda activate walmart-forecast
```

---

## Step 3: Upgrade pip

```bash
pip install --upgrade pip setuptools wheel
```

---

## Step 4: Install Dependencies

### Full Installation (All packages)

```bash
pip install -r requirements.txt
```

**Note**: This may take 5-10 minutes depending on your internet connection.

### Minimal Installation (Core packages only)

If you want to start with essential packages only:

```bash
pip install pandas numpy matplotlib seaborn scipy jupyter
```

---

## Step 5: Install Jupyter Extensions (Optional)

```bash
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

---

## Step 6: Verify Installation

```bash
# Create test script
python -c "
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print('pandas:', pd.__version__)
print('numpy:', np.__version__)
print('matplotlib:', plt.matplotlib.__version__)
print('seaborn:', sns.__version__)
print('\\n✅ All core packages installed successfully!')
"
```

Expected output:
```
pandas: 2.1.4
numpy: 1.26.2
matplotlib: 3.8.2
seaborn: 0.13.0

✅ All core packages installed successfully!
```

---

## Step 7: Launch Jupyter Notebook

```bash
# From project root
jupyter notebook

# Or launch specific notebook
jupyter notebook notebooks/01_eda.ipynb
```

Your browser should open automatically at `http://localhost:8888`

---

## Step 8: Run EDA Notebook

1. Navigate to `notebooks/01_eda.ipynb`
2. Click on the notebook to open it
3. Run all cells: `Cell` → `Run All`

---

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install missing package
pip install <package-name>
```

### Issue: Kernel not found in Jupyter

**Solution**:
```bash
# Install ipykernel
pip install ipykernel

# Add kernel to Jupyter
python -m ipykernel install --user --name=walmart-forecast
```

### Issue: Permission denied

**Solution**:
```bash
# Use --user flag
pip install --user -r requirements.txt
```

### Issue: Prophet installation fails

**Solution**:
```bash
# Prophet requires additional dependencies
# Mac/Linux
brew install cmake

# Then install prophet
pip install prophet
```

---

## Verify Project Setup

```bash
# Check project structure
ls -la

# Expected output:
# config/
# data/
# docs/
# notebooks/
# src/
# reports/
# ...
```

---

## Next Steps

After successful installation:

1. **Run EDA**: `jupyter notebook notebooks/01_eda.ipynb`
2. **Review Config**: `cat config/config.yaml`
3. **Check Data**: `ls -lh data/raw/`

---

## Uninstall / Cleanup

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv/

# Or with conda
conda deactivate
conda remove -n walmart-forecast --all
```

---

## Additional Resources

- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/index.html
- **Seaborn Tutorial**: https://seaborn.pydata.org/tutorial.html
- **Jupyter Notebook**: https://jupyter-notebook.readthedocs.io/

---

## Support

If you encounter any issues:

**Contact**: Ing. Daniel Varela Perez
📧 bedaniele0@gmail.com
📱 +52 55 4189 3428

---

**Status**: Installation guide complete ✅
**Last Updated**: December 4, 2024
