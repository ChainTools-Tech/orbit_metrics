import logging

from cosmos_exporter.metrics import *
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
            for wallet in node.get('wallets', []):
                wallet_type = wallet.get('type', 'unknown')  # Get type or default to 'unknown'
                balance = api_client.fetch_wallet_balance(wallet['address'], node['main_denom'])
                wallet_balance_gauge.labels(chain=node['name'],
                                            chain_id=chain_id,
                                            wallet=wallet['address'],
                                            type=wallet_type).set(balance)
                logger.debug(f'Fetched wallet balance {balance} in denom {node["main_denom"]} for wallet {wallet["address"]}')

            # Fetch validator stakes
            for validator in node.get('validators', []):
                stake = api_client.fetch_validator_stake(validator['validator_id'])
                validator_stake_gauge.labels(chain=node['name'],
                                             chain_id=chain_id,
                                             validator=validator['validator_id']).set(stake)
                logger.debug(f'Fetched stake {stake} for validator {validator["validator_id"]}')

            # Fetch distribution parameters
            params = api_client.fetch_distribution_params()
            if params:
                community_tax_gauge.labels(chain=node['name']).set(float(params['community_tax']))
                base_proposer_reward_gauge.labels(chain=node['name']).set(float(params['base_proposer_reward']))
                bonus_proposer_reward_gauge.labels(chain=node['name']).set(float(params['bonus_proposer_reward']))
                withdraw_addr_enabled_gauge.labels(chain=node['name']).set(
                    1 if params['withdraw_addr_enabled'] else 0)

            # Fetch mint parameters
            mint_params = api_client.fetch_mint_params()
            if mint_params:
                mint_denom = mint_params['mint_denom']  # Keep mint_denom as a string
                inflation_rate_change_gauge.labels(chain=node['name'], mint_denom=mint_denom).set(float(mint_params['inflation_rate_change']))
                inflation_max_gauge.labels(chain=node['name'], mint_denom=mint_denom).set(float(mint_params['inflation_max']))
                inflation_min_gauge.labels(chain=node['name'], mint_denom=mint_denom).set(float(mint_params['inflation_min']))
                goal_bonded_gauge.labels(chain=node['name'], mint_denom=mint_denom).set(float(mint_params['goal_bonded']))
                blocks_per_year_gauge.labels(chain=node['name'], mint_denom=mint_denom).set(int(mint_params['blocks_per_year']))

            # Fetch slashing parameters
            slashing_params = api_client.fetch_slashing_params()
            if slashing_params:
                signed_blocks_window_gauge.labels(chain=node['name']).set(int(slashing_params['signed_blocks_window']))
                min_signed_per_window_gauge.labels(chain=node['name']).set(float(slashing_params['min_signed_per_window']))
                downtime_jail_duration_gauge.labels(chain=node['name']).set(int(slashing_params['downtime_jail_duration'].replace('s', '')))  # Convert from "3600s" to int
                slash_fraction_double_sign_gauge.labels(chain=node['name']).set(float(slashing_params['slash_fraction_double_sign']))
                slash_fraction_downtime_gauge.labels(chain=node['name']).set(float(slashing_params['slash_fraction_downtime']))

            # Fetch staking parameters
            staking_params = api_client.fetch_staking_params()
            if staking_params:
                bond_denom = staking_params['bond_denom']  # Keep bond_denom as a string
                unbonding_time_gauge.labels(chain=node['name'], bond_denom=bond_denom).set(int(staking_params['unbonding_time'].replace('s', '')))
                max_validators_gauge.labels(chain=node['name'], bond_denom=bond_denom).set(int(staking_params['max_validators']))
                max_entries_gauge.labels(chain=node['name'], bond_denom=bond_denom).set(int(staking_params['max_entries']))
                historical_entries_gauge.labels(chain=node['name'], bond_denom=bond_denom).set(int(staking_params['historical_entries']))

            # Fetch staking pool data
            pool_data = api_client.fetch_staking_pool()
            if pool_data:
                bonded_tokens_gauge.labels(chain=node['name']).set(int(pool_data['bonded_tokens']))
                not_bonded_tokens_gauge.labels(chain=node['name']).set(int(pool_data['not_bonded_tokens']))

        except Exception as e:
            logger.error(f"Failed to fetch metrics for {node['name']}: {e}")
