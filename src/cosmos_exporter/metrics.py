from prometheus_client import Gauge


# Define metrics
chain_height_gauge = Gauge('blockchain_chain_height',
                           'Current block height of the blockchain',
                           ['chain', 'chain_id', 'host'])

wallet_balance_gauge = Gauge('wallet_balance',
                             'Balance of the wallet in the blockchain',
                             ['chain', 'chain_id', 'wallet', 'type'])

validator_stake_gauge = Gauge('validator_stake',
                              'Amount of stake on a validator',
                              ['chain', 'chain_id', 'validator'])