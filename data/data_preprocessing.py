import pandas as pd
import numpy as np
from data.data_fetcher import get_raw_data


def preprocess_data(symbol="BTC-USD"):
    df = get_raw_data(symbol)

    # -------------------------
    # FIX 1: Flatten columns (CRITICAL)
    # -------------------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # -------------------------
    # FIX 2: Date handling
    # -------------------------
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df.set_index("Date", inplace=True)

    # -------------------------
    # FIX 3: Force numeric columns safely
    # -------------------------
    required_cols = ["Open", "High", "Low", "Close", "Volume"]

    for col in required_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(subset=["Close"], inplace=True)

    # -------------------------
    # Feature Engineering
    # -------------------------
    df["Returns"] = df["Close"].pct_change()
    df["Log_Returns"] = np.log(df["Close"] / df["Close"].shift(1))

    df["MA_7"] = df["Close"].rolling(window=7).mean()
    df["MA_30"] = df["Close"].rolling(window=30).mean()

    df["Volatility"] = df["Returns"].rolling(window=30).std()

    df.dropna(inplace=True)

    return df
