import logging
from typing import Dict, Any, List, Optional

from orbit_metrics.metrics import *
from orbit_metrics.api_client import APIClient

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Class to collect metrics from a blockchain node."""

    def __init__(self, node_config: Dict[str, Any]):
        """
        Initialize the metrics collector.

        Args:
            node_config: Configuration for the node
        """
        self.node_config = node_config
        self.node_name = node_config['name']
        self.api_client = APIClient(node_config['api_url'])
        self.main_denom = node_config['main_denom']
        logger.info(f"Initialized metrics collector for node {self.node_name}")

    def collect_chain_metrics(self) -> None:
        """Collect basic chain metrics like height and chain ID."""
        try:
            # Fetch chain height
            latest_height = self.api_client.fetch_chain_height()
            chain_id = self.api_client.chain_id or self.api_client.fetch_chain_id()
            moniker = self.api_client.moniker

            if latest_height is not None and chain_id and moniker:
                # Use moniker in the metrics instead of host
                chain_height_gauge.labels(
                    chain=self.node_name,
                    chain_id=chain_id,
                    host=moniker
                ).set(latest_height)
                logger.debug(
                    f'Fetched chain height {latest_height} for chain {chain_id} on node {self.node_name} with moniker {moniker}')
            else:
                logger.warning(f"Could not collect chain metrics for {self.node_name}: missing data")
        except Exception as e:
            logger.error(f"Error collecting chain metrics for {self.node_name}: {e}", exc_info=True)

    def collect_wallet_metrics(self) -> None:
        """Collect wallet balance metrics."""
        try:
            for wallet in self.node_config.get('wallets', []):
                wallet_address = wallet['address']
                wallet_type = wallet.get('type', 'unknown')  # Get type or default to 'unknown'

                balance = self.api_client.fetch_wallet_balance(wallet_address, self.main_denom)
                if balance is not None:
                    chain_id = self.api_client.chain_id or self.api_client.fetch_chain_id()
                    if chain_id:
                        wallet_balance_gauge.labels(
                            chain=self.node_name,
                            chain_id=chain_id,
                            wallet=wallet_address,
                            type=wallet_type
                        ).set(balance)
                        logger.debug(
                            f'Fetched wallet balance {balance} in denom {self.main_denom} for wallet {wallet_address}')
                    else:
                        logger.warning(f"Could not record wallet balance for {wallet_address}: missing chain_id")
                else:
                    logger.warning(f"Could not fetch wallet balance for {wallet_address}")
        except Exception as e:
            logger.error(f"Error collecting wallet metrics for {self.node_name}: {e}", exc_info=True)

    def collect_validator_metrics(self) -> None:
        """Collect validator stake metrics."""
        try:
            for validator in self.node_config.get('validators', []):
                validator_id = validator['validator_id']

                stake = self.api_client.fetch_validator_stake(validator_id)
                if stake is not None:
                    chain_id = self.api_client.chain_id or self.api_client.fetch_chain_id()
                    if chain_id:
                        validator_stake_gauge.labels(
                            chain=self.node_name,
                            chain_id=chain_id,
                            validator=validator_id
                        ).set(stake)
                        logger.debug(f'Fetched stake {stake} for validator {validator_id}')
                    else:
                        logger.warning(f"Could not record validator stake for {validator_id}: missing chain_id")
                else:
                    logger.warning(f"Could not fetch validator stake for {validator_id}")
        except Exception as e:
            logger.error(f"Error collecting validator metrics for {self.node_name}: {e}", exc_info=True)

    def collect_distribution_metrics(self) -> None:
        """Collect distribution parameter metrics."""
        try:
            params = self.api_client.fetch_distribution_params()
            if params:
                try:
                    community_tax_gauge.labels(chain=self.node_name).set(float(params['community_tax']))
                    base_proposer_reward_gauge.labels(chain=self.node_name).set(float(params['base_proposer_reward']))
                    bonus_proposer_reward_gauge.labels(chain=self.node_name).set(float(params['bonus_proposer_reward']))
                    withdraw_addr_enabled_gauge.labels(chain=self.node_name).set(
                        1 if params['withdraw_addr_enabled'] else 0)
                    logger.debug(f'Fetched distribution parameters for {self.node_name}')
                except (KeyError, ValueError) as e:
                    logger.error(f"Error processing distribution parameters for {self.node_name}: {e}")
            else:
                logger.warning(f"Could not fetch distribution parameters for {self.node_name}")
        except Exception as e:
            logger.error(f"Error collecting distribution metrics for {self.node_name}: {e}", exc_info=True)

    def collect_mint_metrics(self) -> None:
        """Collect mint parameter metrics."""
        try:
            mint_params = self.api_client.fetch_mint_params()
            if mint_params:
                try:
                    mint_denom = mint_params['mint_denom']  # Keep mint_denom as a string
                    inflation_rate_change_gauge.labels(chain=self.node_name, mint_denom=mint_denom).set(
                        float(mint_params['inflation_rate_change']))
                    inflation_max_gauge.labels(chain=self.node_name, mint_denom=mint_denom).set(
                        float(mint_params['inflation_max']))
                    inflation_min_gauge.labels(chain=self.node_name, mint_denom=mint_denom).set(
                        float(mint_params['inflation_min']))
                    goal_bonded_gauge.labels(chain=self.node_name, mint_denom=mint_denom).set(
                        float(mint_params['goal_bonded']))
                    blocks_per_year_gauge.labels(chain=self.node_name, mint_denom=mint_denom).set(
                        int(mint_params['blocks_per_year']))
                    logger.debug(f'Fetched mint parameters for {self.node_name}')
                except (KeyError, ValueError) as e:
                    logger.error(f"Error processing mint parameters for {self.node_name}: {e}")
            else:
                logger.warning(f"Could not fetch mint parameters for {self.node_name}")
        except Exception as e:
            logger.error(f"Error collecting mint metrics for {self.node_name}: {e}", exc_info=True)

    def collect_slashing_metrics(self) -> None:
        """Collect slashing parameter metrics."""
        try:
            slashing_params = self.api_client.fetch_slashing_params()
            if slashing_params:
                try:
                    signed_blocks_window_gauge.labels(chain=self.node_name).set(
                        int(slashing_params['signed_blocks_window']))
                    min_signed_per_window_gauge.labels(chain=self.node_name).set(
                        float(slashing_params['min_signed_per_window']))

                    # Convert duration string to integer seconds
                    downtime_duration = slashing_params['downtime_jail_duration']
                    if isinstance(downtime_duration, str) and downtime_duration.endswith('s'):
                        downtime_seconds = int(downtime_duration.replace('s', ''))
                    else:
                        downtime_seconds = int(downtime_duration)

                    downtime_jail_duration_gauge.labels(chain=self.node_name).set(downtime_seconds)
                    slash_fraction_double_sign_gauge.labels(chain=self.node_name).set(
                        float(slashing_params['slash_fraction_double_sign']))
                    slash_fraction_downtime_gauge.labels(chain=self.node_name).set(
                        float(slashing_params['slash_fraction_downtime']))
                    logger.debug(f'Fetched slashing parameters for {self.node_name}')
                except (KeyError, ValueError) as e:
                    logger.error(f"Error processing slashing parameters for {self.node_name}: {e}")
            else:
                logger.warning(f"Could not fetch slashing parameters for {self.node_name}")
        except Exception as e:
            logger.error(f"Error collecting slashing metrics for {self.node_name}: {e}", exc_info=True)

    def collect_staking_metrics(self) -> None:
        """Collect staking parameter metrics."""
        try:
            staking_params = self.api_client.fetch_staking_params()
            if staking_params:
                try:
                    bond_denom = staking_params['bond_denom']  # Keep bond_denom as a string

                    # Convert duration string to integer seconds
                    unbonding_time = staking_params['unbonding_time']
                    if isinstance(unbonding_time, str) and unbonding_time.endswith('s'):
                        unbonding_seconds = int(unbonding_time.replace('s', ''))
                    else:
                        unbonding_seconds = int(unbonding_time)

                    unbonding_time_gauge.labels(chain=self.node_name, bond_denom=bond_denom).set(unbonding_seconds)
                    max_validators_gauge.labels(chain=self.node_name, bond_denom=bond_denom).set(
                        int(staking_params['max_validators']))
                    max_entries_gauge.labels(chain=self.node_name, bond_denom=bond_denom).set(
                        int(staking_params['max_entries']))
                    historical_entries_gauge.labels(chain=self.node_name, bond_denom=bond_denom).set(
                        int(staking_params['historical_entries']))
                    logger.debug(f'Fetched staking parameters for {self.node_name}')
                except (KeyError, ValueError) as e:
                    logger.error(f"Error processing staking parameters for {self.node_name}: {e}")
            else:
                logger.warning(f"Could not fetch staking parameters for {self.node_name}")
        except Exception as e:
            logger.error(f"Error collecting staking metrics for {self.node_name}: {e}", exc_info=True)

    def collect_staking_pool_metrics(self) -> None:
        """Collect staking pool metrics."""
        try:
            pool_data = self.api_client.fetch_staking_pool()
            if pool_data:
                try:
                    bonded_tokens_gauge.labels(chain=self.node_name).set(int(pool_data['bonded_tokens']))
                    not_bonded_tokens_gauge.labels(chain=self.node_name).set(int(pool_data['not_bonded_tokens']))
                    logger.debug(f'Fetched staking pool data for {self.node_name}')
                except (KeyError, ValueError) as e:
                    logger.error(f"Error processing staking pool data for {self.node_name}: {e}")
            else:
                logger.warning(f"Could not fetch staking pool data for {self.node_name}")
        except Exception as e:
            logger.error(f"Error collecting staking pool metrics for {self.node_name}: {e}", exc_info=True)

    def collect_all_metrics(self) -> None:
        """Collect all metrics for this node."""
        logger.info(f"Collecting metrics for node {self.node_name}")

        # Collect each type of metric, handling exceptions for each
        self.collect_chain_metrics()
        self.collect_wallet_metrics()
        self.collect_validator_metrics()
        self.collect_distribution_metrics()
        self.collect_mint_metrics()
        self.collect_slashing_metrics()
        self.collect_staking_metrics()
        self.collect_staking_pool_metrics()

        # Log API client statistics
        api_stats = self.api_client.get_api_stats()
        logger.debug(f"API stats for {self.node_name}: {api_stats}")

        logger.info(f"Finished collecting metrics for node {self.node_name}")


def fetch_metrics(config: Dict[str, Any]) -> None:
    """
    Fetch metrics for all nodes in the configuration.

    Args:
        config: Application configuration
    """
    logger.info("Starting metrics collection cycle")

    try:
        # Create a collector for each node and collect metrics
        for node_config in config['nodes']:
            try:
                collector = MetricsCollector(node_config)
                collector.collect_all_metrics()
            except Exception as e:
                logger.error(f"Error collecting metrics for node {node_config.get('name', 'unknown')}: {e}",
                             exc_info=True)

        logger.info("Metrics collection cycle completed successfully")
    except Exception as e:
        logger.error(f"Fatal error in metrics collection cycle: {e}", exc_info=True)