import pytest
from cosmos_exporter.config import load_config

def test_load_config_valid():
    config = load_config("config.yml")  # Replace with a valid config file path
    assert config is not None
    assert "nodes" in config
    assert len(config["nodes"]) > 0

def test_load_config_invalid():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_config.yml")
