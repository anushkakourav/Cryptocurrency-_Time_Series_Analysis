# =========================================================
# config.py
# Central configuration & constants
# =========================================================

# Supported cryptocurrencies
CRYPTO_LIST = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD"
}

# Default date range (can be overridden)
DEFAULT_START_DATE = "2020-01-01"
DEFAULT_END_DATE = None  # None = today

# Rolling window sizes
ROLLING_WINDOWS = {
    "short": 20,
    "long": 50
}

# Volatility window
VOLATILITY_WINDOW = 30

# Forecast horizon (days)
FORECAST_DAYS = 30

# Plot colors (consistent across project)
COLORS = {
    "Bitcoin": "#f7931a",
    "Ethereum": "#627eea",
    "Positive": "#2ea043",
    "Negative": "#f85149"
}
