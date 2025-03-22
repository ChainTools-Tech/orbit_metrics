# Docker Support for Orbit Metrics

This document explains how to run Orbit Metrics in a Docker container.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)

## Quick Start

### Using Docker Compose (Recommended)

1. Create a `config` directory in your project root and place your `config.yml` file inside it:

```bash
mkdir -p config
cp your-config.yml config/config.yml
```

2. Start the container:

```bash
docker-compose up -d
```

3. Check the logs:

```bash
docker-compose logs -f
```

### Using Docker Directly

1. Build the Docker image:

```bash
docker build -t orbit-metrics .
```

2. Run the container:

```bash
docker run -d \
  --name orbit-metrics \
  -p 8000:8000 \
  -v $(pwd)/config:/app/config \
  -e CONFIG_PATH=/app/config/config.yml \
  -e LOG_LEVEL=INFO \
  orbit-metrics
```

## Configuration

### Environment Variables

The Docker container supports the following environment variables:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `CONFIG_PATH` | Path to the configuration file inside the container | `/app/config/config.yml` |
| `LOG_FILE` | Path to the log file inside the container | `/var/log/orbit_metrics/orbit_metrics.log` |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `INFO` |

### Volumes

Mount these volumes for persistent data and configuration:

- `/app/config`: Directory containing your configuration files
- `/var/log/orbit_metrics`: Directory for log files

### Ports

- `8000`: Default Prometheus metrics endpoint (or as configured in your `config.yml`)

## Integration with Prometheus

Add the following to your Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'orbit_metrics'
    static_configs:
      - targets: ['orbit-metrics:8000']  # Use the container name if in the same network
```

## Docker Compose with Full Monitoring Stack

For a complete setup including Prometheus and Grafana, you can use this extended docker-compose.yml:

```yaml
version: '3'

services:
  orbit-metrics:
    build: .
    container_name: orbit-metrics
    ports:
      - "8000:8000"
    volumes:
      - ./config:/app/config
      - orbit_metrics_logs:/var/log/orbit_metrics
    environment:
      - CONFIG_PATH=/app/config/config.yml
      - LOG_LEVEL=INFO
    restart: unless-stopped
    networks:
      - monitoring_network

  prometheus:
    image: prom/prometheus
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped
    networks:
      - monitoring_network

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped
    networks:
      - monitoring_network

networks:
  monitoring_network:

volumes:
  orbit_metrics_logs:
  prometheus_data:
  grafana_data:
```

## Building Multi-Architecture Images

To build images for different architectures (e.g., ARM for Raspberry Pi):

```bash
docker buildx create --name mybuilder --use
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t yourusername/orbit-metrics:latest --push .
```

## Troubleshooting

### Container won't start

Check the logs:

```bash
docker logs orbit-metrics
```

### Can't access metrics

Verify the port mapping and network configuration:

```bash
docker inspect orbit-metrics | grep IPAddress
curl <container-ip>:8000
```

### Permission issues with log files

The container runs as a non-root user. Ensure the log directory is writable:

```bash
docker exec -it orbit-metrics ls -la /var/log/orbit_metrics
```