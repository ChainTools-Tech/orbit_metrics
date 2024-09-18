from unittest.mock import patch
from cosmos_exporter.exporter import fetch_metrics  # Adjust import based on your structure

def test_fetch_metrics():
    mock_config = {
        "nodes": [
            {
                "name": "ChainA",
                "api_url": "http://api.chainA.com",
                "main_denom": "udvpn",
                "wallets": [
                    {"address": "addressA1", "type": "validator"}
                ],
                "validators": [
                    {"validator_id": "validatorA1"}
                ]
            }
        ]
    }

    # Setup your mock data here or adjust based on how you structure the function
    with patch("cosmos_exporter.api_client.APIClient") as MockAPIClient:
        mock_client = MockAPIClient.return_value
        mock_client.fetch_chain_height.return_value = 18722229
        mock_client.fetch_chain_id.return_value = "bitsong-2b"

        # Add wallet and validator mocks if necessary

        # Call your fetch_metrics function
        fetch_metrics(mock_config)  # Pass a mocked configuration

        # Check expected behavior, e.g., if metrics are updated correctly
        # Use assertions to check that correct methods were called
