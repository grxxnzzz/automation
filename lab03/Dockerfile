FROM python:3.11-slim

# Install cron and coreutils (for "date -d")
RUN apt-get update && apt-get install -y cron coreutils && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy main files
COPY currency_exchange_rate.py /app/
COPY cronjob /app/cronjob
COPY entrypoint.sh /app/entrypoint.sh

# Install Python dependencies
RUN pip install --no-cache-dir requests

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Setup data folder for results
RUN mkdir -p /app/data

ENTRYPOINT ["/app/entrypoint.sh"]