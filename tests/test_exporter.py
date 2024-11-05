from unittest.mock import patch, MagicMock
from orbit_metrics.exporter import fetch_metrics


def test_fetch_metrics():
    mock_config = {
        "nodes": [
            {
                "name": "ChainA",
                "api_url": "http://api.chainA.com",
                "main_denom": "udenom",
                "wallets": [
                    {"address": "addressA1", "type": "validator"}
                ],
                "validators": [
                    {"validator_id": "validatorA1"}
                ]
            }
        ]
    }

    with patch("orbit_metrics.api_client.APIClient") as MockAPIClient:
        mock_client = MockAPIClient.return_value

        # Mock the return values for each method
        mock_client.fetch_chain_height.return_value = 18722229
        mock_client.fetch_distribution_params.return_value = {
            "community_tax": "0.020000000000000000",
            "base_proposer_reward": "0.010000000000000000",
            "bonus_proposer_reward": "0.040000000000000000",
            "withdraw_addr_enabled": True
        }
        mock_client.fetch_mint_params.return_value = {
            "mint_denom": "ubtsg",
            "inflation_rate_change": "0.130000000000000000",
            "inflation_max": "0.100000000000000000",
            "inflation_min": "0.070000000000000000",
            "goal_bonded": "0.670000000000000000",
            "blocks_per_year": "5733820"
        }
        mock_client.fetch_slashing_params.return_value = {
            "signed_blocks_window": "10000",
            "min_signed_per_window": "0.050000000000000000",
            "downtime_jail_duration": "3600s",
            "slash_fraction_double_sign": "0.050000000000000000",
            "slash_fraction_downtime": "0.010000000000000000"
        }
        mock_client.fetch_staking_pool.return_value = {
            "not_bonded_tokens": "10968485993366",
            "bonded_tokens": "74343129493578"
        }

        # Call your fetch_metrics function with the mock configuration
        fetch_metrics(mock_config)

        # Assert the expected method calls
        mock_client.fetch_distribution_params.assert_called_once()
        mock_client.fetch_chain_height.assert_called_once()
        mock_client.fetch_mint_params.assert_called_once()
        mock_client.fetch_slashing_params.assert_called_once()
        mock_client.fetch_staking_pool.assert_called_once()
