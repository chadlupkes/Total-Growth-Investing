# Total Growth Investing — Raw Data Collector

Purpose
- A minimal, zero-cost starter to automate raw data collection for your strategy.
- Uses Yahoo Finance via the open `yfinance` Python library (no paid API keys required).
- Outputs per-ticker raw JSON and an aggregated CSV you can use as the canonical raw-data source.

Quickstart (local)
1. Clone the repo
2. Create a virtualenv and install:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
3. Run the fetch script:
   python scripts/fetch_raw_data.py --tickers samples/tickers.csv --out data/raw/raw_data.csv --history

What the script does
- Reads tickers from CSV (one ticker per line or with header `ticker`)
- Fetches ticker.info and (optionally) 1 year historical prices via yfinance
- Saves per-ticker JSON: data/raw/{TICKER}.json
- Writes an aggregated CSV: data/raw/raw_data.csv

Why this first
- Zero budget, robust, and easy to expand.
- Enough raw fields to reproduce most ranking calculations you currently do in Sheets.

Next steps (recommended)
- Confirm the fields you rely on in Sheets. I will map your formulas to a data model.
- Add normalization + validation of fetched fields (some tickers have missing keys).
- Add Google Sheets integration (gspread) or a lightweight REST API (FastAPI) to provide data to apps.
- Add unit tests for the ranking computations translated from your Sheets.
- Schedule runs with GitHub Actions or a small cloud function for remote automation.

Notes on data sources
- yfinance (Yahoo) is free and good for many use-cases but is not guaranteed as an official API.
- When you scale or need more consistent coverage, we can explore Alpha Vantage, Finnhub, or paid providers.

License
- MIT (see LICENSE)
