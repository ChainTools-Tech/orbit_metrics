FROM python:3.9-slim

# Set up working directory
WORKDIR /app

# Install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the application
RUN pip install --no-cache-dir -e .

# Create directory for logs
RUN mkdir -p /var/log/orbit_metrics

# Create a non-root user to run the application
RUN adduser --disabled-password --gecos "" orbit
RUN chown -R orbit:orbit /var/log/orbit_metrics
USER orbit

# Expose Prometheus metrics port (configurable via environment variable)
EXPOSE 8000

# Set environment variables with defaults
ENV CONFIG_PATH=/app/config/config.yml
ENV LOG_FILE=/var/log/orbit_metrics/orbit_metrics.log
ENV LOG_LEVEL=INFO

# Command to run the application
CMD ["sh", "-c", "orbit_metrics --config $CONFIG_PATH --log-file $LOG_FILE --log-level $LOG_LEVEL"]