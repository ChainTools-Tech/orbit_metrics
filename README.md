# Orbit Metrics

## Overview

**Orbit Metrics** is a monitoring tool for Cosmos-based blockchains that collects and exports key metrics related to chain height, wallet balances, validator stakes, and various parameters. It is designed to work seamlessly with Prometheus, allowing for easy visualization and analysis of blockchain data.

## Features

- Fetch chain height and ID from multiple nodes
- Monitor wallet balances for specific addresses
- Collect validator stake amounts
- Retrieve and expose blockchain parameters from various APIs
- Compatible with Prometheus for metrics collection

## Installation

1. **Clone the repository:**

```bash
   git clone https://github.com/YourUsername/orbit_metrics.git
   cd orbit_metrics
````


2. Create a virtual environment (optional but recommended):

```bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
`
3. Install Orbit Metrics and all required packages:

```bash
pip install .
```


## Configuration

Before running the exporter, you need to create a configuration file named config.yml. Below is an example configuration file:

```yaml

nodes:
  - name: BitSong
    api_url: http://api.bitsong.com
    main_denom: ubtsg
    wallets:
      - address: bitsong_wallet_address
        type: validator
    validators:
      - validator_id: bitsongvaloper1...
      
  - name: Sentinel
    api_url: http://api.sentinel.com
    main_denom: sentineldenom
    wallets:
      - address: sentinel_wallet_address
        type: savings
    validators:
      - validator_id: sentinelvaloper1...
```

Configuration Fields
```
nodes: A list of blockchain nodes to monitor.
    name: A friendly name for the node.
    api_url: The base URL of the API endpoint.
    main_denom: The main denomination used for the blockchain.
    wallets: A list of wallets to monitor.
        address: The address of the wallet.
        type: Type of wallet (e.g., validator, savings).
    validators: A list of validators to monitor.
        validator_id: The ID of the validator.
```

## Usage

Run the exporter using the command line:

```bash
python -m orbit_metrics --config config.yml --log-file orbit_metrics.log --log-level DEBUG
```

## Command-Line Options
```bash
--config: Path to the configuration file.
--log-file: Path to the log file.
--log-level: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
```


## Metrics

The exporter exposes the following metrics to Prometheus:

| Metric Name                            | Label(s)                                      | Description                                                           | Data Type |
|----------------------------------------|-----------------------------------------------|-----------------------------------------------------------------------|-----------|
| `orbit_chain_height`                   | `chain`, `chain_id`, `moniker`                | Current height of the blockchain.                                     | Gauge     |
| `orbit_wallet_balance`                 | `chain`, `chain_id`, `wallet`, `type`         | Balance of the specified wallet address.                              | Gauge     |
| `orbit_validator_stake`                | `chain`, `chain_id`, `validator`, `moniker`   | Amount of stake for the specified validator.                          | Gauge     |
| `orbit_community_tax`                  | `chain`, `moniker`                            | Community tax rate for the chain.                                     | Gauge     |
| `orbit_base_proposer_reward`           | `chain`, `moniker`                            | Base proposer reward rate for the chain.                              | Gauge     |
| `orbit_bonus_proposer_reward`          | `chain`, `moniker`                            | Bonus proposer reward rate for the chain.                             | Gauge     |
| `orbit_withdraw_addr_enabled`          | `chain`, `moniker`                            | Indicator of whether withdrawal addresses are enabled.                | Gauge     |
| `orbit_mint_inflation_rate_change`     | `chain`, `mint_denom`, `moniker`              | Inflation rate change for minting.                                    | Gauge     |
| `orbit_slashing_signed_blocks_window`  | `chain`, `moniker`                            | Signed blocks window for slashing.                                    | Gauge     |
| `orbit_staking_unbonding_time`         | `chain`, `bond_denom`, `moniker`              | Unbonding time for staked tokens (in seconds).                        | Gauge     |
| `orbit_staking_pool_bonded_tokens`     | `chain`, `moniker`                            | Amount of bonded tokens in the staking pool.                          | Gauge     |
| `orbit_staking_pool_not_bonded_tokens` | `chain`, `moniker`                            | Amount of not bonded tokens in the staking pool.                      | Gauge     |


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.


## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
Internal tag: 020