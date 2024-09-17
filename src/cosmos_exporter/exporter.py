import logging

from cosmos_exporter.metrics import chain_height_gauge, wallet_balance_gauge, validator_stake_gauge
from cosmos_exporter.api_client import APIClient


logger = logging.getLogger(__name__)


def fetch_metrics(config):
    for node in config['nodes']:
        try:
            api_client = APIClient(node['api_url'])

            # Fetch chain height
            latest_height = api_client.fetch_chain_height()
            chain_id = api_client.fetch_chain_id()  # Fetch the chain ID as well
            chain_height_gauge.labels(chain=node['name'],
                                      chain_id=chain_id,
                                      host=node['host']).set(latest_height)
            logger.debug(f'Fetched chain height {latest_height} for chain {chain_id} on node {node["name"]}')

            # Fetch wallet balances
            for wallet in node['wallets']:
                wallet_type = wallet.get('type', 'unknown')  # Get type or default to 'unknown'
                balance = api_client.fetch_wallet_balance(wallet['address'], node['main_denom'])
                wallet_balance_gauge.labels(chain=node['name'],
                                            chain_id=chain_id,
                                            wallet=wallet['address'],
                                            type=wallet_type).set(balance)
                logger.debug(f'Fetched wallet balance {balance} in denom {node['main_denom']} for wallet {wallet["address"]}')

            # Fetch validator stakes
            for validator in node['validators']:
                stake = api_client.fetch_validator_stake(validator['validator_id'])
                validator_stake_gauge.labels(chain=node['name'],
                                             chain_id=chain_id,
                                             validator=validator['validator_id']).set(stake)
                logger.debug(f'Fetched stake {stake} for validator {validator["validator_id"]}')

        except Exception as e:
            logger.error(f"Failed to fetch metrics for {node['name']}: {e}")