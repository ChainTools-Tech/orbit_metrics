import logging
import yaml
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ConfigValidationError(Exception):
    """Exception raised for errors in the configuration."""
    pass


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dict containing the configuration

    Raises:
        FileNotFoundError: If the configuration file does not exist
        yaml.YAMLError: If the YAML is malformed
    """
    logger.debug(f"Loading configuration from {config_path}")
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.debug("Configuration loaded successfully")
            return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in configuration file: {e}")
        raise


def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate the configuration structure and contents.

    Args:
        config: Configuration dictionary to validate

    Raises:
        ConfigValidationError: If the configuration is invalid
    """
    # Check if the config has a nodes section
    if not config or not isinstance(config, dict):
        raise ConfigValidationError("Configuration must be a dictionary")

    if 'nodes' not in config:
        raise ConfigValidationError("Configuration must have a 'nodes' section")

    if not isinstance(config['nodes'], list) or not config['nodes']:
        raise ConfigValidationError("'nodes' must be a non-empty list")

    # Validate each node configuration
    for i, node in enumerate(config['nodes']):
        if not isinstance(node, dict):
            raise ConfigValidationError(f"Node at index {i} must be a dictionary")

        # Required fields
        required_fields = ['name', 'api_url', 'main_denom']
        for field in required_fields:
            if field not in node:
                raise ConfigValidationError(
                    f"Node '{node.get('name', f'at index {i}')}' is missing required field '{field}'")

        # Validate wallets
        if 'wallets' in node:
            if not isinstance(node['wallets'], list):
                raise ConfigValidationError(f"Wallets for node '{node['name']}' must be a list")

            for j, wallet in enumerate(node['wallets']):
                if not isinstance(wallet, dict):
                    raise ConfigValidationError(f"Wallet at index {j} for node '{node['name']}' must be a dictionary")
                if 'address' not in wallet:
                    raise ConfigValidationError(
                        f"Wallet at index {j} for node '{node['name']}' is missing required field 'address'")

        # Validate validators
        if 'validators' in node:
            if not isinstance(node['validators'], list):
                raise ConfigValidationError(f"Validators for node '{node['name']}' must be a list")

            for j, validator in enumerate(node['validators']):
                if not isinstance(validator, dict):
                    raise ConfigValidationError(
                        f"Validator at index {j} for node '{node['name']}' must be a dictionary")
                if 'validator_id' not in validator:
                    raise ConfigValidationError(
                        f"Validator at index {j} for node '{node['name']}' is missing required field 'validator_id'")

    logger.debug("Configuration validation successful")