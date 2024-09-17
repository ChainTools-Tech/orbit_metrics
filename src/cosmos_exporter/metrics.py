from prometheus_client import Gauge


chain_height_gauge = Gauge('cosmos_exporter_chain_height',
                           'Current block height of the blockchain',
                           ['chain', 'chain_id', 'host'])

wallet_balance_gauge = Gauge('cosmos_exporter_wallet_balance',
                             'Balance of the wallet in the blockchain',
                             ['chain', 'chain_id', 'wallet', 'type'])

validator_stake_gauge = Gauge('cosmos_exporter_validator_stake',
                              'Amount of stake on a validator',
                              ['chain', 'chain_id', 'validator'])