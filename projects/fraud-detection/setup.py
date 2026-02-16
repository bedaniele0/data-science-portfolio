"""
============================================================================
setup.py - Package Configuration for Fraud Detection System
============================================================================
Configuración para instalación del paquete y CLI commands

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Metodología: DVP-PRO
============================================================================
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
requirements_path = this_directory / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="fraud-detection-system",
    version="1.0.0",
    author="Ing. Daniel Varela Perez",
    author_email="bedaniele0@gmail.com",
    description="Fraud Detection System using Random Forest and Real-time Monitoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielvarela/fraud-detection-system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
            "ipython>=8.0.0",
            "ipykernel>=6.0.0",
        ],
        "mlops": [
            "mlflow>=2.8.0",
            "optuna>=3.0.0",
            "shap>=0.42.0",
        ],
        "monitoring": [
            "evidently>=0.4.0",
            "prometheus-client>=0.18.0",
        ],
        "api": [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "python-jose[cryptography]>=3.3.0",
            "passlib[bcrypt]>=1.7.4",
            "python-multipart>=0.0.6",
        ],
        "all": [
            # Dev
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
            # MLOps
            "mlflow>=2.8.0",
            "optuna>=3.0.0",
            "shap>=0.42.0",
            # Monitoring
            "evidently>=0.4.0",
            "prometheus-client>=0.18.0",
            # API
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "python-jose[cryptography]>=3.3.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "fraud-train=models.train_fraud:main",
            "fraud-predict=models.predict:main",
            "fraud-evaluate=models.evaluate:main",
            "fraud-dashboard=utils.cli:fraud_dashboard",
            "fraud-api=utils.cli:fraud_api",
            "fraud-monitor=monitoring.monitoring_run:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.txt"],
    },
    zip_safe=False,
    keywords=[
        "fraud-detection",
        "machine-learning",
        "random-forest",
        "real-time-monitoring",
        "financial-fraud",
        "anomaly-detection",
        "streamlit",
        "fastapi",
        "mlops",
        "dvp-pro"
    ],
    project_urls={
        "Bug Reports": "https://github.com/danielvarela/fraud-detection-system/issues",
        "Source": "https://github.com/danielvarela/fraud-detection-system",
        "Documentation": "https://github.com/danielvarela/fraud-detection-system/blob/main/README.md",
    },
)
