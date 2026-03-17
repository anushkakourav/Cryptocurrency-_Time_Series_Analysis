import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data.data_preprocessing import preprocess_data


# -------------------------------------------------
# Utility
# -------------------------------------------------
def has_enough_data(df, min_rows=50):
    return df is not None and not df.empty and len(df) >= min_rows


# -------------------------------------------------
# Main Render Function
# -------------------------------------------------
def render():
    st.title("📉 Volatility & Risk Analysis")

    # Load processed data
    btc = preprocess_data("BTC-USD")
    eth = preprocess_data("ETH-USD")

    # =================================================
    # Chart 9 & 10: Rolling Volatility
    # =================================================
    st.subheader("Rolling Volatility (14-Day Window)")

    col1, col2 = st.columns(2)

    for name, df, col in [("Bitcoin", btc, col1), ("Ethereum", eth, col2)]:
        with col:
            if has_enough_data(df):
                rolling_vol = df["Returns"].rolling(window=14).std()

                fig, ax = plt.subplots()
                ax.plot(df.index, rolling_vol)
                ax.set_title(f"{name} Rolling Volatility")
                ax.set_xlabel("Date")
                ax.set_ylabel("Volatility")
                st.pyplot(fig)

    # =================================================
    # Chart 11: Bollinger Bands (BTC & ETH side-by-side)
    # =================================================
    st.subheader("Bollinger Bands Comparison (20-Day)")

    col1, col2 = st.columns(2)

    for name, df, col in [("Bitcoin", btc, col1), ("Ethereum", eth, col2)]:
        with col:
            if has_enough_data(df):
                ma_20 = df["Close"].rolling(window=20).mean()
                std_20 = df["Close"].rolling(window=20).std()

                upper = ma_20 + 2 * std_20
                lower = ma_20 - 2 * std_20

                fig, ax = plt.subplots()
                ax.plot(df.index, df["Close"], label="Price")
                ax.plot(df.index, upper, linestyle="--", label="Upper Band")
                ax.plot(df.index, lower, linestyle="--", label="Lower Band")
                ax.set_title(f"{name} Bollinger Bands")
                ax.legend()
                st.pyplot(fig)

    # =================================================
    # Chart 12: High–Low Price Spread
    # =================================================
    st.subheader("Daily High–Low Price Spread")

    col1, col2 = st.columns(2)

    for name, df, col in [("Bitcoin", btc, col1), ("Ethereum", eth, col2)]:
        with col:
            if has_enough_data(df):
                spread = df["High"] - df["Low"]

                fig, ax = plt.subplots()
                ax.plot(df.index, spread)
                ax.set_title(f"{name} High–Low Spread")
                ax.set_xlabel("Date")
                ax.set_ylabel("Spread")
                st.pyplot(fig)

    # =================================================
    # Chart 13: Volatility Comparison
    # =================================================
    st.subheader("Volatility Comparison")

    vol_data = {
        "Bitcoin": btc["Returns"].std() * np.sqrt(252),
        "Ethereum": eth["Returns"].std() * np.sqrt(252),
    }

    vol_df = pd.DataFrame.from_dict(vol_data, orient="index", columns=["Annualized Volatility"])

    fig, ax = plt.subplots()
    vol_df.plot(kind="bar", legend=False, ax=ax)
    ax.set_ylabel("Volatility")
    ax.set_title("BTC vs ETH Volatility")
    st.pyplot(fig)

    # =================================================
    # Chart 14: Risk vs Return
    # =================================================
    st.subheader("Risk vs Return")

    risk_return = pd.DataFrame({
        "Risk": [btc["Returns"].std(), eth["Returns"].std()],
        "Return": [btc["Returns"].mean(), eth["Returns"].mean()]
    }, index=["Bitcoin", "Ethereum"])

    fig, ax = plt.subplots()
    ax.scatter(risk_return["Risk"], risk_return["Return"])

    for i, txt in enumerate(risk_return.index):
        ax.annotate(txt, (risk_return["Risk"][i], risk_return["Return"][i]))

    ax.set_xlabel("Risk (Std Dev)")
    ax.set_ylabel("Mean Return")
    ax.set_title("Risk vs Return Comparison")
    st.pyplot(fig)

    # =================================================
    # Chart 15: Returns Distribution
    # =================================================
    st.subheader("Returns Distribution")

    fig, ax = plt.subplots()
    ax.boxplot(
        [btc["Returns"].dropna(), eth["Returns"].dropna()],
        labels=["Bitcoin", "Ethereum"]
    )
    ax.set_ylabel("Returns")
    ax.set_title("Returns Distribution Comparison")
    st.pyplot(fig)

    # =========================================================
    # Volatility: Executive Summary
    # =========================================================
    st.subheader("📌Volatility Summary Insights")

    st.success(
        """
**Key Volatility Insights**

• **Ethereum** generally exhibits higher volatility compared to **Bitcoin**, indicating greater risk exposure.  
• **Bollinger Band width** highlights periods of intense price movement and heightened market uncertainty.  
• **High–low price spreads** effectively capture intraday risk behavior across both crypto assets.  
• The **risk–return tradeoff** differs between Bitcoin and Ethereum, emphasizing asset-specific risk profiles.
"""
    )


