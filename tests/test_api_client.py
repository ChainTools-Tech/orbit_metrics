from unittest.mock import patch
from cosmos_exporter.api_client import APIClient

def test_fetch_chain_height():
    api_client = APIClient("http://fake_api_url")

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "block": {
                "header": {
                    "height": "18722229"
                }
            }
        }

        height = api_client.fetch_chain_height()
        assert height == 18722229
