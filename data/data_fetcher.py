import yfinance as yf
import pandas as pd
import os

CACHE_DIR = "data/cached_data"
os.makedirs(CACHE_DIR, exist_ok=True)


def get_raw_data(symbol="BTC-USD"):
    cache_file = os.path.join(CACHE_DIR, f"{symbol}.csv")

    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
    else:
        df = yf.download(symbol, start="2023-01-01")
        df.reset_index(inplace=True)
        df.to_csv(cache_file, index=False)

    return df


