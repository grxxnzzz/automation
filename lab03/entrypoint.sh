#!/bin/sh
set -e

echo "=== Saving environment variables for cron ==="
env > /etc/environment

echo "=== Creating cron log file ==="
touch /var/log/cron.log
chmod 666 /var/log/cron.log

echo "=== Installing cron jobs ==="
crontab /app/cronjob

echo "=== Starting cron service ==="
cron

echo "=== Tailing log file ==="
tail -f /var/log/cron.log