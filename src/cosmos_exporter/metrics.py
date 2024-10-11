from prometheus_client import Gauge

# /cosmos/base/tendermint/v1beta1/blocks/latest
chain_height_gauge = Gauge('cosmos_exporter_chain_height',
                           'Current block height of the blockchain',
                           ['chain', 'chain_id', 'host'])

# /cosmos/bank/v1beta1/balances/{wallet_address}
wallet_balance_gauge = Gauge('cosmos_exporter_wallet_balance',
                             'Balance of the wallet in the blockchain',
                             ['chain', 'chain_id', 'wallet', 'type'])

# /cosmos/staking/v1beta1/validators/{validator_address}
validator_stake_gauge = Gauge('cosmos_exporter_validator_stake',
                              'Amount of stake on a validator',
                              ['chain', 'chain_id', 'validator'])


"""
/cosmos/distribution/v1beta1/params
"""
community_tax_gauge = Gauge(
    'cosmos_exporter_community_tax',
    'Community tax percentage',
    ['chain']  # You can add other labels if needed
)

base_proposer_reward_gauge = Gauge(
    'cosmos_exporter_base_proposer_reward',
    'Base proposer reward percentage',
    ['chain']
)

bonus_proposer_reward_gauge = Gauge(
    'cosmos_exporter_bonus_proposer_reward',
    'Bonus proposer reward percentage',
    ['chain']
)

withdraw_addr_enabled_gauge = Gauge(
    'cosmos_exporter_withdraw_addr_enabled',
    'Is withdraw address enabled (1 for true, 0 for false)',
    ['chain']
)


"""
/cosmos/mint/v1beta1/params
"""
inflation_rate_change_gauge = Gauge(
    'cosmos_exporter_inflation_rate_change',
    'Inflation rate change percentage',
    ['chain', 'mint_denom']  # Include mint_denom as a label
)

inflation_max_gauge = Gauge(
    'cosmos_exporter_inflation_max',
    'Maximum inflation percentage',
    ['chain', 'mint_denom']
)

inflation_min_gauge = Gauge(
    'cosmos_exporter_inflation_min',
    'Minimum inflation percentage',
    ['chain', 'mint_denom']
)

goal_bonded_gauge = Gauge(
    'cosmos_exporter_goal_bonded',
    'Goal bonded percentage',
    ['chain', 'mint_denom']
)

blocks_per_year_gauge = Gauge(
    'cosmos_exporter_blocks_per_year',
    'Number of blocks per year',
    ['chain', 'mint_denom']
)


"""
/cosmos/slashing/v1beta1/params
"""
signed_blocks_window_gauge = Gauge(
    'cosmos_exporter_signed_blocks_window',
    'Number of signed blocks in the window',
    ['chain']
)

min_signed_per_window_gauge = Gauge(
    'cosmos_exporter_min_signed_per_window',
    'Minimum signed per window percentage',
    ['chain']
)

downtime_jail_duration_gauge = Gauge(
    'cosmos_exporter_downtime_jail_duration',
    'Downtime jail duration in seconds',
    ['chain']
)

slash_fraction_double_sign_gauge = Gauge(
    'cosmos_exporter_slash_fraction_double_sign',
    'Slash fraction for double signing',
    ['chain']
)

slash_fraction_downtime_gauge = Gauge(
    'cosmos_exporter_slash_fraction_downtime',
    'Slash fraction for downtime',
    ['chain']
)


"""
/cosmos/staking/v1beta1/params
"""
unbonding_time_gauge = Gauge(
    'cosmos_exporter_unbonding_time',
    'Unbonding time in seconds',
    ['chain', 'bond_denom']  # Include bond_denom as a label
)

max_validators_gauge = Gauge(
    'cosmos_exporter_max_validators',
    'Maximum number of validators',
    ['chain', 'bond_denom']
)

max_entries_gauge = Gauge(
    'cosmos_exporter_max_entries',
    'Maximum entries in the validator set',
    ['chain', 'bond_denom']
)

historical_entries_gauge = Gauge(
    'cosmos_exporter_historical_entries',
    'Number of historical entries for validators',
    ['chain', 'bond_denom']
)


"""
/cosmos/staking/v1beta1/pool
"""
bonded_tokens_gauge = Gauge(
    'cosmos_exporter_bonded_tokens',
    'Total bonded tokens in the staking pool',
    ['chain']
)

not_bonded_tokens_gauge = Gauge(
    'cosmos_exporter_not_bonded_tokens',
    'Total not bonded tokens in the staking pool',
    ['chain']
)