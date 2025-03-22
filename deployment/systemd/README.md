# Running Orbit Metrics as a Systemd Service

This guide explains how to set up Orbit Metrics as a systemd service on Linux systems.

## Installation

1. **Create a dedicated user for running the service**

```bash
sudo useradd -r -s /bin/false orbit-metrics
```

2. **Create necessary directories**

```bash
# Create configuration directory
sudo mkdir -p /etc/orbit_metrics

# Create log directory
sudo mkdir -p /var/log/orbit_metrics
sudo chown orbit-metrics:orbit-metrics /var/log/orbit_metrics

# Create application directory
sudo mkdir -p /opt/orbit_metrics
```

3. **Install Orbit Metrics**

```bash
# Clone the repository
sudo git clone https://github.com/qf3l3k/orbit_metrics.git /opt/orbit_metrics

# Set up virtual environment
cd /opt/orbit_metrics
sudo python3 -m venv venv
sudo ./venv/bin/pip install -e .

# Set ownership
sudo chown -R orbit-metrics:orbit-metrics /opt/orbit_metrics
```

4. **Create configuration file**

```bash
sudo nano /etc/orbit_metrics/config.yml
```

Add your configuration to this file (see example below).

5. **Install systemd service file**

```bash
# Copy service file
sudo cp /opt/orbit_metrics/systemd/orbit-metrics.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload
```

## Configuration Example

Here's a minimal example configuration:

```yaml
# Global configuration
prometheus:
  port: 8000  # Port for the Prometheus metrics endpoint
refresh_interval: 60  # Seconds between metric updates

# Blockchain nodes to monitor
nodes:
  - name: "CosmosHub"
    api_url: "https://api.cosmos.network"
    main_denom: "uatom"
    validators:
      - validator_id: "cosmosvaloper1..."
    wallets:
      - { address: "cosmos1...", type: "validator" }
```

## Service Management

### Starting the service

```bash
sudo systemctl start orbit-metrics
```

### Checking service status

```bash
sudo systemctl status orbit-metrics
```

### Enabling automatic start at boot

```bash
sudo systemctl enable orbit-metrics
```

### Viewing logs

```bash
# View systemd journal logs
sudo journalctl -u orbit-metrics -f

# View application log file
sudo tail -f /var/log/orbit_metrics/orbit_metrics.log
```

### Restarting the service

```bash
sudo systemctl restart orbit-metrics
```

### Stopping the service

```bash
sudo systemctl stop orbit-metrics
```

## Service Configuration Options

You can modify the systemd service by editing the service file:

```bash
sudo nano /etc/systemd/system/orbit-metrics.service
```

After making changes, reload the daemon:

```bash
sudo systemctl daemon-reload
```

### Common Configuration Adjustments

#### Change resource limits

Uncomment and adjust these lines in the service file:

```
CPUQuota=50%
MemoryLimit=256M
```

#### Set environment variables

Add environment variables if needed:

```
Environment=PYTHONUNBUFFERED=1
```

#### Change restart policy

Modify the restart behavior:

```
Restart=always
RestartSec=30
```

## Troubleshooting

### Service fails to start

1. Check for syntax errors in your configuration:

```bash
sudo -u orbit-metrics /opt/orbit_metrics/venv/bin/orbit_metrics --config /etc/orbit_metrics/config.yml --log-level DEBUG
```

2. Check for permission issues:

```bash
sudo ls -la /var/log/orbit_metrics
sudo ls -la /etc/orbit_metrics
```

3. Verify the Python virtual environment:

```bash
sudo -u orbit-metrics /opt/orbit_metrics/venv/bin/python -V
```

### Service starts but no metrics

1. Verify the Prometheus port is accessible:

```bash
curl http://localhost:8000
```

2. Check if there are any connectivity issues to the blockchain nodes:

```bash
sudo journalctl -u orbit-metrics | grep "Error fetching"
```

### High resource usage

If the service is using too many resources, add resource limits to the service file:

```
CPUQuota=25%
MemoryLimit=128M
IOWeight=500
```

## Security Considerations

The service is configured with several security enhancements:

- Runs as a dedicated non-root user
- Has restricted system access via `ProtectSystem` and `ProtectHome`
- Cannot gain new privileges
- Uses a private /tmp directory

For production deployments, consider:

1. Setting up a firewall to restrict access to the metrics port
2. Configuring TLS with a reverse proxy like Nginx
3. Further restricting the service with additional systemd security options