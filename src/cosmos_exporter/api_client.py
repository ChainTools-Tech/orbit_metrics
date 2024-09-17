import logging
import requests

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_chain_height(self):
        try:
            response = requests.get(f"{self.api_url}/blocks/latest")
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            logger.debug(f'Chain height data retrieved: {data}')
            return int(data['block']['header']['height'])  # Extract height
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching chain height: {e}')
            return None
        except (KeyError, ValueError) as e:
            logger.error(f'Error parsing chain height data: {e}')
            return None

    def fetch_chain_id(self):
        try:
            response = requests.get(f"{self.api_url}/blocks/latest")
            response.raise_for_status()
            data = response.json()
            logger.debug(f'Chain ID data retrieved: {data}')
            return data['block']['header']['chain_id']  # Extract chain_id
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching chain ID: {e}')
            return None
        except (KeyError, ValueError) as e:
            logger.error(f'Error parsing chain ID data: {e}')
            return None

    def fetch_wallet_balance(self, wallet_address, main_denom):
        try:
            response = requests.get(f"{self.api_url}/cosmos/bank/v1beta1/balances/{wallet_address}")
            response.raise_for_status()
            data = response.json()
            logger.debug(f'Wallet balance data retrieved: {data}')

            # Find the balance for the specified main_denom
            for balance in data['balances']:
                if balance['denom'] == main_denom:
                    return float(balance['amount'])

            logger.warning(f'No balance found for denom: {main_denom} in wallet: {wallet_address}')
            return 0.0
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching wallet balance for {wallet_address}: {e}')
            return None
        except (KeyError, ValueError) as e:
            logger.error(f'Error parsing wallet balance data: {e}')
            return None

    def fetch_validator_stake(self, validator_address):
        try:
            response = requests.get(f"{self.api_url}/cosmos/staking/v1beta1/validators/{validator_address}")
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            logger.debug(f'Validator stake data retrieved: {data}')

            # Extract the tokens (stake) from the response
            return float(data['validator']['tokens'])
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching validator stake for {validator_address}: {e}')
            return None
        except (KeyError, ValueError) as e:
            logger.error(f'Error parsing validator stake data: {e}')
            return None
