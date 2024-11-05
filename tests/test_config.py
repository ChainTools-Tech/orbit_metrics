# tests/test_config.py

import pytest
from orbit_metrics.config import load_config

def test_load_config_valid():
    config = load_config("tests/valid_config.yml")  # Replace with a valid config file path
    assert config is not None
    assert "nodes" in config
    assert len(config["nodes"]) > 0

def test_load_config_invalid():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_config.yml")
