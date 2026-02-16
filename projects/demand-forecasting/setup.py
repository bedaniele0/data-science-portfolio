"""
============================================================================
setup.py - Walmart Demand Forecasting Package Setup
============================================================================
Configuración para instalación del proyecto como paquete Python

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Metodología: DVP-PRO
============================================================================
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text(encoding="utf-8").splitlines()
requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]

setup(
    name="walmart-demand-forecasting",
    version="1.2.0",
    author="Ing. Daniel Varela Perez",
    author_email="bedaniele0@gmail.com",
    description="Intelligent demand forecasting system for Walmart using ML and optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielvarela/walmart-demand-forecasting",
    project_urls={
        "Bug Tracker": "https://github.com/danielvarela/walmart-demand-forecasting/issues",
        "Documentation": "https://github.com/danielvarela/walmart-demand-forecasting/blob/main/README.md",
        "Source Code": "https://github.com/danielvarela/walmart-demand-forecasting",
    },
    packages=find_packages(where=".", exclude=["tests", "tests.*", "notebooks", "notebooks.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "jupyter>=1.0.0",
            "ipykernel>=6.20.0",
        ],
        "mlops": [
            "mlflow>=2.9.0",
            "optuna>=3.4.0",
        ],
        "monitoring": [
            "prometheus-client>=0.18.0",
            "evidently>=0.4.0",
        ],
        "all": [
            # Dev tools
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "jupyter>=1.0.0",
            "ipykernel>=6.20.0",
            # MLOps
            "mlflow>=2.9.0",
            "optuna>=3.4.0",
            # Monitoring
            "prometheus-client>=0.18.0",
            "evidently>=0.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "walmart-train=src.models.train_demand:main",
            "walmart-predict=src.models.predict:main",
            "walmart-api=src.api.main:main",
            "walmart-dashboard=src.visualization.dashboard:main",
            "walmart-monitor=src.monitoring.monitoring_run:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.csv", "*.txt"],
    },
    zip_safe=False,
    keywords=[
        "machine-learning",
        "demand-forecasting",
        "time-series",
        "walmart",
        "retail-analytics",
        "inventory-optimization",
        "mlops",
        "fastapi",
        "streamlit",
    ],
    license="MIT",
)
