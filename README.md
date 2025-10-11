# IW03: Task Scheduler (cron)

The script `currency_exchange_rate.py` requests the exchange rate between two currencies on a specified date from a local support service (which is launched via Docker Compose), saves the response in a JSON file in the root folder of the project in the `data/` directory, and logs errors in `error.log`.

## Requirements
- Python 3.8+
- pip
- Library `requests`
- Docker Desktop

## Dependencies (Windows):
```shell
pip install requests
```
> For Docker instructions look at [Lab02 Prep Task Info](./lab02prep_readme.md#how-to-run)

## How to run the project
1. **Clone the repository**
```powershell
git clone https://github.com/grxxnzzz/automation/tree/lab02
cd automation/lab02
```
2. **Create `.env` file with API key (any api key may be written)**
3. **Start the Docker service**
```powershell
docker-compose up -d
```
4. **Run the Python client from Windows**
```powershell
python currency_exchange_rate.py USD EUR 2025-01-01 --key QWERTY123
```
5. **Results**

If successful then you will get report like that:

> OK — result saved in: data/USD_EUR_2025-01-01.json

It will be created in newly made folder `data/` and errors will be stored at `error.log`.

### Request examples:
```powershell
# USD → EUR
python currency_exchange_rate.py USD EUR 2025-01-01 --key QWERTY123

# EUR → RON
python currency_exchange_rate.py EUR RON 2025-03-06 --key QWERTY123
```

# How does script work
The `currency_exchange_rate.py` script is a command-line client that interacts with the Currency Exchange Rate API running in Docker. Its structure is divided into several logical parts:
1. **Argument parsing**
    - The script uses the argparse module to accept input parameters from the command line.
    - Required arguments:
        - `from_currency` – the source currency (e.g., `USD`)
        - `to_currency` – the target currency (e.g., `EUR`)
        - `date` – the date for the exchange rate in `YYYY-MM-DD` format
    - Optional arguments:
        - `--key` – the API key (if not provided, the script tries to read it from the environment variable `API_KEY`).
2. **Building the request**
    - The script constructs the API endpoint URL: 
        ```powershell
        http://localhost:8080/?from=FROM&to=TO&date=DATE
        ```
    - It sends the request using the `requests` library with the API key included in the POST body.
3. **Handling the API response**
    - If the API returns an error (e.g., invalid parameters, unsupported currency, missing key), the script prints a clear error message in the console and also appends it to a log file named `error.log` in the project root.
    - If the request is successful, the response data (exchange rate, currencies, date) is saved in JSON format.
4. **Saving results**
    - The script creates a `data/` directory in the project root if it does not exist.
    - It saves the result to a file named:
        ```powershell
        data/FROM_TO_DATE.json
        ```
    For example: `data/USD_EUR_2025-01-01.json`.
5. **Error logging**
    - All errors are written both to the console and to `error.log` in the root directory, so failed requests can be tracked.

# Summary

!!!to be inserted!!!