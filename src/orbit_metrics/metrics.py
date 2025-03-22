from prometheus_client import Gauge, Counter, Info


# Application info
app_info = Info('orbit_metrics_info', 'Information about the Orbit Metrics exporter')
app_info.info({
    'version': '0.1.0',
    'description': 'Prometheus exporter for Cosmos SDK blockchains'
})

# API metrics
api_requests_total = Counter(
    'orbit_metrics_api_requests_total',
    'Total number of API requests made',
    ['chain', 'endpoint', 'status']
)

api_request_duration = Gauge(
    'orbit_metrics_api_request_duration_seconds',
    'Duration of API requests in seconds',
    ['chain', 'endpoint']
)

# Main chain metrics
chain_height_gauge = Gauge(
    'orbit_metrics_chain_height',
    'Current block height of the blockchain',
    ['chain', 'chain_id', 'host']
)

# Wallet metrics
wallet_balance_gauge = Gauge(
    'orbit_metrics_wallet_balance',
    'Balance of the wallet in the blockchain',
    ['chain', 'chain_id', 'wallet', 'type']
)

# Validator metrics
validator_stake_gauge = Gauge(
    'orbit_metrics_validator_stake',
    'Amount of stake on a validator',
    ['chain', 'chain_id', 'validator']
)

# Distribution parameters
community_tax_gauge = Gauge(
    'orbit_metrics_community_tax',
    'Community tax percentage',
    ['chain']
)

base_proposer_reward_gauge = Gauge(
    'orbit_metrics_base_proposer_reward',
    'Base proposer reward percentage',
    ['chain']
)

bonus_proposer_reward_gauge = Gauge(
    'orbit_metrics_bonus_proposer_reward',
    'Bonus proposer reward percentage',
    ['chain']
)

withdraw_addr_enabled_gauge = Gauge(
    'orbit_metrics_withdraw_addr_enabled',
    'Is withdraw address enabled (1 for true, 0 for false)',
    ['chain']
)

# Mint parameters
inflation_rate_change_gauge = Gauge(
    'orbit_metrics_inflation_rate_change',
    'Inflation rate change percentage',
    ['chain', 'mint_denom']
)

inflation_max_gauge = Gauge(
    'orbit_metrics_inflation_max',
    'Maximum inflation percentage',
    ['chain', 'mint_denom']
)

inflation_min_gauge = Gauge(
    'orbit_metrics_inflation_min',
    'Minimum inflation percentage',
    ['chain', 'mint_denom']
)

goal_bonded_gauge = Gauge(
    'orbit_metrics_goal_bonded',
    'Goal bonded percentage',
    ['chain', 'mint_denom']
)

blocks_per_year_gauge = Gauge(
    'orbit_metrics_blocks_per_year',
    'Number of blocks per year',
    ['chain', 'mint_denom']
)

# Slashing parameters
signed_blocks_window_gauge = Gauge(
    'orbit_metrics_signed_blocks_window',
    'Number of signed blocks in the window',
    ['chain']
)

min_signed_per_window_gauge = Gauge(
    'orbit_metrics_min_signed_per_window',
    'Minimum signed per window percentage',
    ['chain']
)

downtime_jail_duration_gauge = Gauge(
    'orbit_metrics_downtime_jail_duration',
    'Downtime jail duration in seconds',
    ['chain']
)

slash_fraction_double_sign_gauge = Gauge(
    'orbit_metrics_slash_fraction_double_sign',
    'Slash fraction for double signing',
    ['chain']
)

slash_fraction_downtime_gauge = Gauge(
    'orbit_metrics_slash_fraction_downtime',
    'Slash fraction for downtime',
    ['chain']
)

# Staking parameters
unbonding_time_gauge = Gauge(
    'orbit_metrics_unbonding_time',
    'Unbonding time in seconds',
    ['chain', 'bond_denom']
)

max_validators_gauge = Gauge(
    'orbit_metrics_max_validators',
    'Maximum number of validators',
    ['chain', 'bond_denom']
)

max_entries_gauge = Gauge(
    'orbit_metrics_max_entries',
    'Maximum entries in the validator set',
    ['chain', 'bond_denom']
)

historical_entries_gauge = Gauge(
    'orbit_metrics_historical_entries',
    'Number of historical entries for validators',
    ['chain', 'bond_denom']
)

# Staking pool metrics
bonded_tokens_gauge = Gauge(
    'orbit_metrics_bonded_tokens',
    'Total bonded tokens in the staking pool',
    ['chain']
)

not_bonded_tokens_gauge = Gauge(
    'orbit_metrics_not_bonded_tokens',
    'Total not bonded tokens in the staking pool',
    ['chain']
)

# Exporter internal metrics
last_scrape_duration = Gauge(
    'orbit_metrics_last_scrape_duration_seconds',
    'Duration of the last metrics collection in seconds'
)

scrape_failures_total = Counter(
    'orbit_metrics_scrape_failures_total',
    'Total number of scrape failures by chain',
    ['chain']
)

up = Gauge(
    'orbit_metrics_up',
    'Indicates if the exporter is up and running (1 for up, 0 for down)',
    ['chain']
)