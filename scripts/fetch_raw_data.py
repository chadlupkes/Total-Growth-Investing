#!/usr/bin/env python3
"""
Fetch raw market/fundamental data for a list of tickers using yfinance.
Saves per-ticker JSON and an aggregated CSV.

Usage:
  python scripts/fetch_raw_data.py --tickers samples/tickers.csv --out data/raw/raw_data.csv --history
"""
import argparse
import csv
import json
import os
from pathlib import Path
from typing import List, Dict
import time

import pandas as pd
import yfinance as yf

DEFAULT_OUT_DIR = Path("data/raw")


def load_tickers(path: str) -> List[str]:
    pathp = Path(path)
    if not pathp.exists():
        raise FileNotFoundError(f"{path} not found")
    tickers = []
    with open(pathp, newline="") as fh:
        # accept CSV with header 'ticker' or a plain one-column file
        reader = csv.reader(fh)
        for row in reader:
            if not row:
                continue
            value = row[0].strip()
            if value.lower() == "ticker":
                continue
            if value:
                tickers.append(value)
    return tickers


def safe_get(info: Dict, keys: List[str]):
    for k in keys:
        if k in info:
            return info[k]
    return None


def fetch_and_save(tickers: List[str], out_csv: str, out_dir: Path, fetch_history=False):
    out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for i, ticker in enumerate(tickers, start=1):
        print(f"[{i}/{len(tickers)}] fetching {ticker} ...")
        try:
            tk = yf.Ticker(ticker)
            info = tk.info or {}
            # select fields commonly useful for ranking
            rec = {
                "symbol": ticker,
                "shortName": info.get("shortName"),
                "longName": info.get("longName"),
                "currency": info.get("currency"),
                "exchange": info.get("exchange"),
                "regularMarketPrice": info.get("regularMarketPrice"),
                "previousClose": info.get("previousClose"),
                "marketCap": info.get("marketCap"),
                "trailingPE": info.get("trailingPE"),
                "forwardPE": info.get("forwardPE"),
                "priceToBook": info.get("priceToBook"),
                "priceToSalesTrailing12Months": info.get("priceToSalesTrailing12Months"),
                "trailingAnnualDividendYield": info.get("trailingAnnualDividendYield"),
                "beta": info.get("beta"),
                "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
                "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
                "volume": info.get("volume"),
                "averageVolume": info.get("averageVolume"),
                "dividendYield": info.get("dividendYield") or info.get("dividendRate"),
                "returnOnEquity": info.get("returnOnEquity"),
                "totalRevenue": info.get("totalRevenue"),
                "ebitda": info.get("ebitda"),
                "grossMargins": info.get("grossMargins"),
                "profitMargins": info.get("profitMargins"),
            }
            # save raw JSON
            json_path = out_dir / f"{ticker}.json"
            with open(json_path, "w") as jf:
                json.dump(info, jf, indent=2, default=str)

            if fetch_history:
                try:
                    hist = tk.history(period="1y", interval="1d", actions=False)
                    if not hist.empty:
                        hist_path = out_dir / f"{ticker}_1y.csv"
                        hist.to_csv(hist_path)
                except Exception as e:
                    print(f"  warning: failed to fetch history for {ticker}: {e}")

            records.append(rec)
        except Exception as e:
            print(f"  error fetching {ticker}: {e}")
        # be polite
        time.sleep(0.5)

    # make CSV
    if records:
        df = pd.DataFrame(records)
        out_csv_path = Path(out_csv)
        out_csv_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_csv_path, index=False)
        print(f"Wrote combined CSV to {out_csv_path}")
    else:
        print("No records fetched.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", required=True, help="CSV file containing tickers (one per line or header 'ticker')")
    ap.add_argument("--out", default=str(DEFAULT_OUT_DIR / "raw_data.csv"), help="Output aggregated CSV")
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Directory for per-ticker JSON & history")
    ap.add_argument("--history", action="store_true", help="Also fetch 1y historical prices per ticker")
    args = ap.parse_args()

    tickers = load_tickers(args.tickers)
    if not tickers:
        print("No tickers found in the provided file.")
        return
    fetch_and_save(tickers, args.out, Path(args.out_dir), fetch_history=args.history)


if __name__ == "__main__":
    main()
