# Orbit Metrics

A comprehensive Prometheus exporter for Cosmos SDK blockchains.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)

## Overview

**Orbit Metrics** monitors Cosmos-based blockchains by collecting and exporting key metrics related to:
- Chain height and blockchain status
- Wallet balances
- Validator stakes
- Chain parameters (distribution, mint, slashing, staking)
- Pool statistics

The exporter is designed to work seamlessly with Prometheus, enabling easy integration with monitoring stacks like Grafana.

## Features

- **Multi-chain monitoring**: Monitor multiple Cosmos-based chains simultaneously
- **Comprehensive metrics**: Track a wide range of blockchain parameters
- **Robust error handling**: Continue operations even when some data sources are unavailable
- **Efficient API usage**: Implements caching to reduce load on blockchain nodes
- **Flexible configuration**: Configure chains, wallets, and validators through YAML
- **Detailed logging**: Configurable logging to both console and file

## Installation

### Prerequisites

- Python 3.6 or higher
- Prometheus server (for metrics collection)

### Method 1: From Source

1. Clone the repository:
```bash
git clone https://github.com/qf3l3k/orbit_metrics.git
cd orbit_metrics
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install Orbit Metrics:
```bash
pip install .
```

### Method 2: Using pip

```bash
pip install orbit-metrics
```

## Configuration

Create a configuration file named `config.yml`. Here's an example:

```yaml
# Global configuration
prometheus:
  port: 8000  # Port for the Prometheus metrics endpoint
refresh_interval: 60  # Seconds between metric updates

# Blockchain nodes to monitor
nodes:
  - name: "AssetMantle"
    api_url: "https://rest.assetmantle.one:443/"
    main_denom: "umntl"
    validators:
      - validator_id: "mantlevaloper18w60w6fnptk9dhqpl65mzrejmkt0vvr7u5qwp5"
    wallets:
      - { address: "mantle18w60w6fnptk9dhqpl65mzrejmkt0vvr7uty66p", type: "validator" }
      
  - name: "BitSong"
    api_url: "https://api.bitsong.chaintools.tech:443/"
    main_denom: "ubtsg"
    validators:
      - validator_id: "bitsongvaloper1x2slrjfmgxq7qx3xwmsjue73t5ynmwy7jgpdtr"
    wallets:
      - { address: "bitsong1vp9xldhdmjfmnwel7nl6tgy8numduq08qm4jpm", type: "relayer" }
      - { address: "bitsong1x2slrjfmgxq7qx3xwmsjue73t5ynmwy7nvaym7", type: "validator" }
```

### Configuration Options

| Field | Description | Required |
|-------|-------------|----------|
| `prometheus.port` | Port for Prometheus metrics endpoint | No (default: 8000) |
| `refresh_interval` | Seconds between metric updates | No (default: 60) |
| `nodes` | List of blockchain nodes to monitor | Yes |
| `nodes[].name` | Friendly name for the node | Yes |
| `nodes[].api_url` | Base URL of the API endpoint | Yes |
| `nodes[].main_denom` | Main denomination used for the blockchain | Yes |
| `nodes[].wallets` | List of wallets to monitor | No |
| `nodes[].wallets[].address` | Wallet address | Yes |
| `nodes[].wallets[].type` | Type of wallet (e.g., validator, relayer) | No |
| `nodes[].validators` | List of validators to monitor | No |
| `nodes[].validators[].validator_id` | Validator ID | Yes |

## Usage

Run the exporter using the command line:

```bash
orbit_metrics --config config.yml --log-file orbit_metrics.log --log-level INFO
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--config` | Path to the configuration file | Required |
| `--log-file` | Path to the log file | `orbit_metrics.log` |
| `--log-level` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | INFO |
| `--version` | Show version and exit | |

## Available Metrics

Orbit Metrics exposes the following metrics to Prometheus:

### Chain Metrics
- `orbit_metrics_chain_height`: Current height of the blockchain
- `orbit_metrics_up`: Indicates if the exporter successfully connected to the chain

### Wallet Metrics
- `orbit_metrics_wallet_balance`: Balance of the specified wallet address

### Validator Metrics
- `orbit_metrics_validator_stake`: Amount of stake for a validator

### Distribution Parameters
- `orbit_metrics_community_tax`: Community tax rate
- `orbit_metrics_base_proposer_reward`: Base proposer reward rate
- `orbit_metrics_bonus_proposer_reward`: Bonus proposer reward rate
- `orbit_metrics_withdraw_addr_enabled`: Indicates if withdrawal addresses are enabled

### Mint Parameters
- `orbit_metrics_inflation_rate_change`: Inflation rate change for minting
- `orbit_metrics_inflation_max`: Maximum inflation percentage
- `orbit_metrics_inflation_min`: Minimum inflation percentage
- `orbit_metrics_goal_bonded`: Goal bonded percentage
- `orbit_metrics_blocks_per_year`: Number of blocks per year

### Slashing Parameters
- `orbit_metrics_signed_blocks_window`: Signed blocks window for slashing
- `orbit_metrics_min_signed_per_window`: Minimum signed per window percentage
- `orbit_metrics_downtime_jail_duration`: Downtime jail duration in seconds
- `orbit_metrics_slash_fraction_double_sign`: Slash fraction for double signing
- `orbit_metrics_slash_fraction_downtime`: Slash fraction for downtime

### Staking Parameters
- `orbit_metrics_unbonding_time`: Unbonding time in seconds
- `orbit_metrics_max_validators`: Maximum number of validators
- `orbit_metrics_max_entries`: Maximum entries in the validator set
- `orbit_metrics_historical_entries`: Number of historical entries for validators
- `orbit_metrics_bonded_tokens`: Total bonded tokens in the staking pool
- `orbit_metrics_not_bonded_tokens`: Total not bonded tokens in the staking pool

### Exporter Metrics
- `orbit_metrics_info`: Information about the Orbit Metrics exporter
- `orbit_metrics_api_requests_total`: Total number of API requests made
- `orbit_metrics_api_request_duration_seconds`: Duration of API requests
- `orbit_metrics_last_scrape_duration_seconds`: Duration of the last metrics collection
- `orbit_metrics_scrape_failures_total`: Total number of scrape failures by chain

## Prometheus Configuration

Add the following to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'orbit_metrics'
    static_configs:
      - targets: ['localhost:8000']
```

## Grafana Dashboard

A sample Grafana dashboard is available in the `dashboards` directory. Import it into your Grafana instance for a quick start with visualizing the metrics.

## Troubleshooting

### Common Issues

1. **Connection errors**: 
   - Verify the API endpoints in your configuration are correct
   - Check if the nodes are accessible from your network

2. **Missing metrics**:
   - Different Cosmos chains might use different API paths
   - Ensure your node has the required modules enabled

3. **High memory usage**:
   - Adjust the refresh interval to reduce API calls

Check the logs for more detailed error messages.


## Deployment

For deployment instructions:

- [Docker deployment](./deployment/docker)
- [Systemd service deployment](./deployment/systemd)


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Cosmos SDK team for creating a robust blockchain framework
- Prometheus project for their excellent monitoring system
- All contributors to the project