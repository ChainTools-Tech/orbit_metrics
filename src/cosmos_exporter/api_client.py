import logging
import requests

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, api_url):
        self.api_url = api_url
        self.moniker = None
        self.chain_id = None
        self.latest_block_data = None
        self.fetch_node_info()

    def fetch_node_info(self):
        """Fetch node information from the API, trying multiple endpoints."""
        endpoints = [
            f"{self.api_url}/node_info",
            f"{self.api_url}/cosmos/base/tendermint/v1beta1/node_info"
        ]

        for endpoint in endpoints:
            try:
                response = requests.get(endpoint)
                response.raise_for_status()
                data = response.json()
                logger.debug(f'Node info data retrieved from {endpoint}: {data}')

                # Check for the appropriate key based on the endpoint
                node_info_key = 'node_info' if 'node_info' in data else 'default_node_info'

                # Store moniker and chain_id
                self.moniker = data[node_info_key]['moniker']
                self.chain_id = data[node_info_key]['network']

                return  # Exit if successful
            except requests.exceptions.RequestException as e:
                logger.error(f'Error fetching node info from {endpoint}: {e}')
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing node info data from {endpoint}: {e}')

        logger.error("Failed to fetch node info from all endpoints.")

    def fetch_latest_block_data(self):
        """Fetch the latest block data once."""
        try:
            response = requests.get(f"{self.api_url}/cosmos/base/tendermint/v1beta1/blocks/latest")
            response.raise_for_status()
            self.latest_block_data = response.json()
            logger.debug(f'Latest block data block: {self.latest_block_data}')
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching latest block data: {e}')
            self.latest_block_data = None

    def fetch_chain_height(self):
        """Return the chain height from cached data."""
        if self.latest_block_data is None:
            self.fetch_latest_block_data()  # Fetch data if not already fetched
        if self.latest_block_data:
            try:
                return int(self.latest_block_data['block']['header']['height'])  # Extract height
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing chain height data: {e}')
                return None

    def fetch_chain_id(self):
        """Return the chain ID from cached data."""
        if self.latest_block_data is None:
            self.fetch_latest_block_data()  # Fetch data if not already fetched
        if self.latest_block_data:
            try:
                return self.latest_block_data['block']['header']['chain_id']  # Extract chain_id
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

    def fetch_distribution_params(self):
        """Fetch distribution parameters from the API."""
        try:
            response = requests.get(f"{self.api_url}/cosmos/distribution/v1beta1/params")
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            logger.debug(f'Distribution params data retrieved: {data}')
            return data['params']
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching distribution parameters: {e}')
            return None
        except (KeyError, ValueError) as e:
            logger.error(f'Error parsing distribution parameters data: {e}')
            return None

    def fetch_mint_params(self):
        """Fetch mint parameters from the API."""
        try:
            response = requests.get(f"{self.api_url}/cosmos/mint/v1beta1/params")
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            logger.debug(f'Mint params data retrieved: {data}')
            return data['params']
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching mint parameters: {e}')
            return None
        except (KeyError, ValueError) as e:
            logger.error(f'Error parsing mint parameters data: {e}')
            return None

    def fetch_slashing_params(self):
        """Fetch slashing parameters from the API."""
        try:
            response = requests.get(f"{self.api_url}/cosmos/slashing/v1beta1/params")
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            logger.debug(f'Slashing params data retrieved: {data}')
            return data['params']
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching slashing parameters: {e}')
            return None
        except (KeyError, ValueError) as e:
            logger.error(f'Error parsing slashing parameters data: {e}')
            return None

    def fetch_staking_params(self):
        """Fetch staking parameters from the API."""
        try:
            response = requests.get(f"{self.api_url}/cosmos/staking/v1beta1/params")
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            logger.debug(f'Staking params data retrieved: {data}')
            return data['params']
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching staking parameters: {e}')
            return None
        except (KeyError, ValueError) as e:
            logger.error(f'Error parsing staking parameters data: {e}')
            return None

    def fetch_staking_pool(self):
        """Fetch staking pool data from the API."""
        try:
            response = requests.get(f"{self.api_url}/cosmos/staking/v1beta1/pool")
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            logger.debug(f'Staking pool data retrieved: {data}')
            return data['pool']
        except requests.exceptions.RequestException as e:
            logger.error(f'Error fetching staking pool data: {e}')
            return None
        except (KeyError, ValueError) as e:
            logger.error(f'Error parsing staking pool data: {e}')
            return None
