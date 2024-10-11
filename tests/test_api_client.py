import pytest
from unittest.mock import patch, MagicMock
from cosmos_exporter.api_client import APIClient

@pytest.fixture
def api_client():
    return APIClient("http://fake_api_url")

def test_fetch_distribution_params(api_client):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "params": {
                "community_tax": "0.020000000000000000",
                "base_proposer_reward": "0.010000000000000000",
                "bonus_proposer_reward": "0.040000000000000000",
                "withdraw_addr_enabled": True
            }
        }
        mock_get.return_value = mock_response
        mock_get.return_value.status_code = 200

        params = api_client.fetch_distribution_params()
        assert params['community_tax'] == "0.020000000000000000"

def test_fetch_mint_params(api_client):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "params": {
                "mint_denom": "ubtsg",
                "inflation_rate_change": "0.130000000000000000",
                "inflation_max": "0.100000000000000000",
                "inflation_min": "0.070000000000000000",
                "goal_bonded": "0.670000000000000000",
                "blocks_per_year": "5733820"
            }
        }
        mock_get.return_value = mock_response
        mock_get.return_value.status_code = 200

        params = api_client.fetch_mint_params()
        assert params['mint_denom'] == "ubtsg"

def test_fetch_slashing_params(api_client):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "params": {
                "signed_blocks_window": "10000",
                "min_signed_per_window": "0.050000000000000000",
                "downtime_jail_duration": "3600s",
                "slash_fraction_double_sign": "0.050000000000000000",
                "slash_fraction_downtime": "0.010000000000000000"
            }
        }
        mock_get.return_value = mock_response
        mock_get.return_value.status_code = 200

        params = api_client.fetch_slashing_params()
        assert params['signed_blocks_window'] == "10000"

def test_fetch_staking_pool(api_client):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "pool": {
                "not_bonded_tokens": "10968485993366",
                "bonded_tokens": "74343129493578"
            }
        }
        mock_get.return_value = mock_response
        mock_get.return_value.status_code = 200

        pool = api_client.fetch_staking_pool()
        assert pool['not_bonded_tokens'] == "10968485993366"
