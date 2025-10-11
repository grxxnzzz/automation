#!/usr/bin/env python3
"""
currency_exchange_rate.py

Requests the exchange rate between two currencies on a specified date from a local service,
saves the response to a JSON file in the project root folder in the `data/` directory,
and logs errors to the `error.log` file in the project root.

Usage:
    python lab02/currency_exchange_rate.py FROM TO DATE [--key API_KEY] [--url URL]

Examples:
    python lab02/currency_exchange_rate.py USD EUR 2025-02-01 --key EXAMPLE_API_KEY
    python lab02/currency_exchange_rate.py MDL UAH 2025-03-06
"""
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, date
from pathlib import Path
import sys

import requests

# Parameters
KNOWN_CURRENCIES = {"MDL", "USD", "EUR", "RON", "RUB", "UAH"}
MIN_DATE = date(2025, 1, 1)
MAX_DATE = date(2025, 9, 15)
DEFAULT_URL = "http://localhost:8080/"

# Paths (root dir - parent of lab02)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
ERROR_LOG = PROJECT_ROOT / "error.log"


def log_error(msg: str) -> None:
    ts = datetime.now().isoformat(sep=" ", timespec="seconds")
    line = f"{ts} - {msg}\n"
    try:
        ERROR_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(ERROR_LOG, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        # If error.log cannot be opened, print to stderr anyway
        print(f"[ERROR] Failed to write to {ERROR_LOG}: {e}", file=sys.stderr)
    print(f"[ERROR] {msg}", file=sys.stderr)


def validate_currency(c: str) -> str:
    if not re.fullmatch(r"[A-Za-z]{3}", c):
        raise ValueError("The currency code must consist of 3 letters (e.g. USD)")
    c = c.upper()
    if c not in KNOWN_CURRENCIES:
        raise ValueError(f"Unknown currency: {c}. Supported: {', '.join(sorted(KNOWN_CURRENCIES))}")
    return c


def validate_date(s: str) -> str:
    try:
        d = datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("The date must be in the format YYYY-MM-DD.")
    if d < MIN_DATE or d > MAX_DATE:
        raise ValueError(f"Date outside the acceptable period: {MIN_DATE.isoformat()} — {MAX_DATE.isoformat()}")
    return d.isoformat()


def request_rate(api_url: str, api_key: str, frm: str, to: str, when: str, timeout: int = 10):
    """
    Performs a POST request (as in the curl example: GET parameters in the URL, the request itself is POST with a key field).
    """
    params = {"from": frm, "to": to, "date": when}
    try:
        resp = requests.post(api_url, params=params, data={"key": api_key}, timeout=timeout)
    except requests.RequestException as e:
        raise ConnectionError(f"Error connecting to {api_url}: {e}") from e

    if resp.status_code != 200:
        raise ConnectionError(f"HTTP {resp.status_code} from server")

    try:
        payload = resp.json()
    except ValueError:
        raise ValueError("The server response is not JSON")

    return payload


def save_json(payload, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)


def parse_args():
    p = argparse.ArgumentParser(description="Request exchange rate and save result in data/")
    p.add_argument("from_currency", help="Source currency (USD, EUR, MDL, etc.)")
    p.add_argument("to_currency", help="Target currency")
    p.add_argument("date", help="Date in YYYY-MM-DD format (period 2025-01-01 — 2025-09-15)")
    p.add_argument("--key", "-k", help="API key (if not specified, the API_KEY environment variable will be used)")
    p.add_argument("--url", "-u", default=DEFAULT_URL, help=f"Service URL (default {DEFAULT_URL})")
    return p.parse_args()


def main():
    args = parse_args()

    # API key: priority — argument, then environment
    api_key = args.key or os.getenv("API_KEY")
    if not api_key:
        msg = "API key not provided. Specify --key or set the API_KEY environment variable."
        log_error(msg)
        sys.exit(2)

    # Arguments validation
    try:
        frm = validate_currency(args.from_currency.upper())
        to = validate_currency(args.to_currency.upper())
        when = validate_date(args.date)
    except ValueError as e:
        log_error(str(e))
        sys.exit(2)

    # Request
    try:
        payload = request_rate(args.url, api_key, frm, to, when)
    except Exception as e:
        log_error(str(e))
        sys.exit(1)

    # Check whether the service returned an error
    if isinstance(payload, dict) and payload.get("error"):
        log_error(f"API returned error: {payload.get('error')}")
        # Also save the error response in the log file (useful for debugging).
        try:
            save_json(payload, DATA_DIR / f"error_{frm}_{to}_{when}.json")
        except Exception:
            pass
        sys.exit(1)

    # Save the successful response (all JSON)
    filename = f"{frm}_{to}_{when}.json"
    out_path = DATA_DIR / filename
    try:
        save_json(payload, out_path)
    except Exception as e:
        log_error(f"Failed to save file {out_path}: {e}")
        sys.exit(1)

    print(f"OK — result saved in: {out_path}")


if __name__ == "__main__":
    main()