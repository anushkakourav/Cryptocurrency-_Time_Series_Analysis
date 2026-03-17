# =========================================================
# helpers.py
# Reusable helper functions across the project
# =========================================================

import pandas as pd


def has_enough_data(df, min_rows=30):
    """
    Check whether a dataframe has sufficient data for analysis.
    """
    if df is None or df.empty:
        return False
    return len(df) >= min_rows


def safe_pct(value, decimals=2):
    """
    Safely format a percentage value.
    """
    try:
        return f"{value * 100:.{decimals}f}%"
    except Exception:
        return "N/A"


def safe_float(value, decimals=4):
    """
    Safely format a float value.
    """
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return "N/A"


def ensure_datetime(df, column="Date"):
    """
    Ensure a column is in datetime format.
    """
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


def drop_na(df, columns=None):
    """
    Drop NA values safely from dataframe.
    """
    if columns:
        return df.dropna(subset=columns)
    return df.dropna()
