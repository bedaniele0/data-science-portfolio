from pathlib import Path

import yaml


def test_config_loads():
    config_path = Path('configs/config.yaml')
    assert config_path.exists()
    cfg = yaml.safe_load(config_path.read_text())
    assert 'paths' in cfg


def test_feature_pipeline_import():
    from src import feature_pipeline  # noqa: F401
