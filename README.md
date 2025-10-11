# IW03: Task Scheduler (cron)

The script `currency_exchange_rate.py` is used to automatically request and store currency exchange rates between two currencies for a specific date.
In this lab, the script is executed automatically by a cron job inside a Docker container, eliminating the need for manual runs.

The script connects to a local Currency Exchange Rate service (from Lab02) that provides exchange rates for several currencies.
All results are saved as `.json` files in the `data/` directory, while possible errors are logged to `error.log`.

## Requirements
- Python 3.8+
- pip
- Library `requests`
- Docker Desktop

## Dependencies (Windows):
```shell
pip install requests
```
> For Docker & Setup instructions (or readme) look at [Lab02 Prep](.../lab02/lab02prep_readme.md)

## How to run the project
1. **Clone the repository**
```powershell
git clone https://github.com/grxxnzzz/automation/tree/lab02
cd automation/lab03
```
2. **Create `.env` file with API key (any api key may be written)**
3. **Start the Docker service**
```powershell
docker-compose up --build -d
```
4. **Verify that cron is running**
```powershell
docker logs lab03_cron
```

# Cron job configuration
```bash
0 6 * * * python3 /app/currency_exchange_rate.py MDL EUR $(date -d "yesterday" +\%Y-\%m-\%d) --key QWERTY123 >> /var/log/cron.log 2>&1
0 17 * * 5 python3 /app/currency_exchange_rate.py MDL USD $(date -d "7 days ago" +\%Y-\%m-\%d) --key QWERTY123 >> /var/log/cron.log 2>&1
```
- Every day at 06:00 AM — fetches MDL → EUR for yesterday
- Every Friday at 17:00 (5 PM) — fetches MDL → USD for 7 days ago
- All logs are stored in `/var/log/cron.log`.

# Summary

This laboratory work demonstrates how to use a task scheduler (cron) inside a Docker environment to automate the execution of a Python script.
The containerized approach ensures a consistent runtime environment and allows periodic tasks (such as fetching exchange rates) to run without manual intervention.

The integration between Python, Docker, and cron provides a practical example of automation and system orchestration — fundamental skills for DevOps and backend engineering.