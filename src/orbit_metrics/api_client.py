import logging
import requests
import time
from typing import Dict, Any, List, Optional, Union, Tuple
from functools import lru_cache

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, api_url: str):
        """
        Initialize the API client.

        Args:
            api_url: Base URL for the API
        """
        self.api_url = api_url.rstrip('/')  # Remove trailing slash if present
        self.moniker: Optional[str] = None
        self.chain_id: Optional[str] = None
        self.latest_block_data: Optional[Dict[str, Any]] = None

        # Track API call statistics
        self.api_calls = 0
        self.api_errors = 0
        self.last_api_call = 0

        # Cache of API responses to prevent duplicate calls
        self._cache: Dict[str, Tuple[float, Any]] = {}

        # Cache expiration time (in seconds)
        self.cache_expiration = 60  # Default to 60 seconds

        # Call initialize to set up initial data
        self.initialize()

    def initialize(self) -> None:
        """Initialize the client by fetching node information."""
        self.fetch_node_info()

    def make_api_call(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                      cache: bool = True, cache_ttl: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Make an API call with caching, retry logic, and error handling.

        Args:
            endpoint: API endpoint to call (without the base URL)
            params: Optional query parameters
            cache: Whether to cache the response
            cache_ttl: Time-to-live for cache entry (in seconds)

        Returns:
            Response data as a dictionary or None if the call failed
        """
        # Use default cache TTL if not specified
        if cache_ttl is None:
            cache_ttl = self.cache_expiration

        # Construct the full URL
        if endpoint.startswith('http'):
            url = endpoint  # Endpoint is already a full URL
        else:
            # Ensure the endpoint starts with a slash
            if not endpoint.startswith('/'):
                endpoint = f'/{endpoint}'
            url = f"{self.api_url}{endpoint}"

        # Check cache first if caching is enabled
        cache_key = f"{url}:{str(params)}"
        if cache and cache_key in self._cache:
            timestamp, data = self._cache[cache_key]
            if time.time() - timestamp <= cache_ttl:
                logger.debug(f"Cache hit for {url}")
                return data

        # Track API call metrics
        self.api_calls += 1
        self.last_api_call = time.time()

        # Make the API call with retry logic
        retries = 3
        backoff = 1  # Initial backoff in seconds

        for attempt in range(retries):
            try:
                logger.debug(f"Making API call to {url} (attempt {attempt + 1}/{retries})")

                response = requests.get(url, params=params, timeout=10)  # Add a timeout
                response.raise_for_status()

                data = response.json()

                # Cache the response if caching is enabled
                if cache:
                    self._cache[cache_key] = (time.time(), data)

                return data

            except requests.exceptions.RequestException as e:
                self.api_errors += 1
                logger.error(f"Error making API call to {url} (attempt {attempt + 1}/{retries}): {e}")

                # If this is the last retry, re-raise the exception
                if attempt == retries - 1:
                    logger.error(f"Failed all {retries} attempts to call {url}")
                    return None

                # Wait before retrying with exponential backoff
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
            except (ValueError, KeyError) as e:
                self.api_errors += 1
                logger.error(f"Error parsing response from {url}: {e}")
                return None

    def fetch_node_info(self) -> None:
        """Fetch node information from the API, trying multiple endpoints."""
        endpoints = [
            "/node_info",
            "/cosmos/base/tendermint/v1beta1/node_info"
        ]

        for endpoint in endpoints:
            data = self.make_api_call(endpoint, cache=True, cache_ttl=300)  # Cache for 5 minutes
            if not data:
                continue

            try:
                # Check for the appropriate key based on the endpoint
                node_info_key = 'node_info' if 'node_info' in data else 'default_node_info'

                # Store moniker and chain_id
                self.moniker = data[node_info_key]['moniker']
                self.chain_id = data[node_info_key]['network']
                logger.info(f"Connected to node {self.moniker} on chain {self.chain_id}")
                return
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing node info data from {endpoint}: {e}')

        logger.error("Failed to fetch node info from all endpoints.")

    def fetch_latest_block_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetch the latest block data.

        Returns:
            The latest block data or None if the call failed
        """
        if self.latest_block_data is None:
            self.latest_block_data = self.make_api_call(
                "/cosmos/base/tendermint/v1beta1/blocks/latest",
                cache=True,
                cache_ttl=10  # Short cache time for block data
            )
        return self.latest_block_data

    def fetch_chain_height(self) -> Optional[int]:
        """
        Return the chain height from cached data.

        Returns:
            The chain height or None if the data is not available
        """
        data = self.fetch_latest_block_data()
        if data:
            try:
                return int(data['block']['header']['height'])
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing chain height data: {e}')
        return None

    def fetch_chain_id(self) -> Optional[str]:
        """
        Return the chain ID from cached data.

        Returns:
            The chain ID or None if the data is not available
        """
        # First try to use the cached value
        if self.chain_id:
            return self.chain_id

        # Otherwise, try to get it from the latest block data
        data = self.fetch_latest_block_data()
        if data:
            try:
                return data['block']['header']['chain_id']
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing chain ID data: {e}')
        return None

    def fetch_wallet_balance(self, wallet_address: str, main_denom: str) -> Optional[float]:
        """
        Fetch the balance of a wallet.

        Args:
            wallet_address: The address of the wallet
            main_denom: The main denomination to query

        Returns:
            The wallet balance or None if the call failed
        """
        data = self.make_api_call(
            f"/cosmos/bank/v1beta1/balances/{wallet_address}",
            cache=True,
            cache_ttl=30  # Cache for 30 seconds
        )

        if data:
            try:
                # Find the balance for the specified main_denom
                for balance in data['balances']:
                    if balance['denom'] == main_denom:
                        return float(balance['amount'])

                logger.warning(f'No balance found for denom: {main_denom} in wallet: {wallet_address}')
                return 0.0
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing wallet balance data: {e}')
        return None

    def fetch_validator_stake(self, validator_address: str) -> Optional[float]:
        """
        Fetch the stake of a validator.

        Args:
            validator_address: The address of the validator

        Returns:
            The validator stake or None if the call failed
        """
        data = self.make_api_call(
            f"/cosmos/staking/v1beta1/validators/{validator_address}",
            cache=True,
            cache_ttl=60  # Cache for 60 seconds
        )

        if data:
            try:
                return float(data['validator']['tokens'])
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing validator stake data: {e}')
        return None

    def fetch_distribution_params(self) -> Optional[Dict[str, Any]]:
        """
        Fetch distribution parameters from the API.

        Returns:
            The distribution parameters or None if the call failed
        """
        data = self.make_api_call(
            "/cosmos/distribution/v1beta1/params",
            cache=True,
            cache_ttl=300  # Cache for 5 minutes
        )

        if data:
            try:
                return data['params']
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing distribution parameters data: {e}')
        return None

    def fetch_mint_params(self) -> Optional[Dict[str, Any]]:
        """
        Fetch mint parameters from the API.

        Returns:
            The mint parameters or None if the call failed
        """
        data = self.make_api_call(
            "/cosmos/mint/v1beta1/params",
            cache=True,
            cache_ttl=300  # Cache for 5 minutes
        )

        if data:
            try:
                return data['params']
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing mint parameters data: {e}')
        return None

    def fetch_slashing_params(self) -> Optional[Dict[str, Any]]:
        """
        Fetch slashing parameters from the API.

        Returns:
            The slashing parameters or None if the call failed
        """
        data = self.make_api_call(
            "/cosmos/slashing/v1beta1/params",
            cache=True,
            cache_ttl=300  # Cache for 5 minutes
        )

        if data:
            try:
                return data['params']
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing slashing parameters data: {e}')
        return None

    def fetch_staking_params(self) -> Optional[Dict[str, Any]]:
        """
        Fetch staking parameters from the API.

        Returns:
            The staking parameters or None if the call failed
        """
        data = self.make_api_call(
            "/cosmos/staking/v1beta1/params",
            cache=True,
            cache_ttl=300  # Cache for 5 minutes
        )

        if data:
            try:
                return data['params']
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing staking parameters data: {e}')
        return None

    def fetch_staking_pool(self) -> Optional[Dict[str, Any]]:
        """
        Fetch staking pool data from the API.

        Returns:
            The staking pool data or None if the call failed
        """
        data = self.make_api_call(
            "/cosmos/staking/v1beta1/pool",
            cache=True,
            cache_ttl=60  # Cache for 60 seconds
        )

        if data:
            try:
                return data['pool']
            except (KeyError, ValueError) as e:
                logger.error(f'Error parsing staking pool data: {e}')
        return None

    def get_api_stats(self) -> Dict[str, Any]:
        """
        Get statistics about API calls.

        Returns:
            Dictionary with API call statistics
        """
        return {
            'api_calls': self.api_calls,
            'api_errors': self.api_errors,
            'error_rate': self.api_errors / max(1, self.api_calls),
            'last_api_call': self.last_api_call,
            'cache_size': len(self._cache)
        }