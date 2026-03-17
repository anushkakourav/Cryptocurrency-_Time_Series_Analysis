import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from data.data_preprocessing import preprocess_data


# -------------------------------------------------
# Utility functions
# -------------------------------------------------
def has_enough_data(df, min_rows=50):
    return df is not None and not df.empty and len(df) >= min_rows


def calculate_kpis(df):
    roi = (df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100
    volatility = df["Returns"].std() * np.sqrt(252) * 100

    cumulative = (1 + df["Returns"]).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100

    return roi, volatility, max_drawdown


# -------------------------------------------------
# Main render function
# -------------------------------------------------
def render():
    st.title("📌 Decision Support & Insights Dashboard")

    # Load data
    btc = preprocess_data("BTC-USD")
    eth = preprocess_data("ETH-USD")

    # =================================================
    # 23 & 24: Best / Worst Performing Crypto
    # =================================================
    st.subheader("Best & Worst Performing Crypto")

    returns = {
        "Bitcoin": (btc["Close"].iloc[-1] / btc["Close"].iloc[0] - 1) * 100,
        "Ethereum": (eth["Close"].iloc[-1] / eth["Close"].iloc[0] - 1) * 100,
    }

    perf_df = pd.DataFrame.from_dict(
        returns, orient="index", columns=["Total Return (%)"]
    )

    fig, ax = plt.subplots()
    perf_df.plot(kind="bar", legend=False, ax=ax)
    ax.set_ylabel("Return (%)")
    ax.set_title("Crypto Performance Comparison")
    st.pyplot(fig)

    # =================================================
    # 25: Monthly Returns Heatmap (SIDE-BY-SIDE)
    # =================================================
    st.subheader("Monthly Returns Heatmap Comparison")

    col1, col2 = st.columns(2)

    def plot_heatmap(df, title):
        monthly = df["Returns"].resample("M").sum().dropna()
        heatmap_df = monthly.to_frame("Returns")
        heatmap_df["Year"] = heatmap_df.index.year
        heatmap_df["Month"] = heatmap_df.index.month
        pivot = heatmap_df.pivot(index="Year", columns="Month", values="Returns")

        fig, ax = plt.subplots()
        sns.heatmap(pivot, cmap="RdYlGn", center=0, ax=ax)
        ax.set_title(title)
        st.pyplot(fig)

    with col1:
        if has_enough_data(btc):
            plot_heatmap(btc, "Bitcoin Monthly Returns")

    with col2:
        if has_enough_data(eth):
            plot_heatmap(eth, "Ethereum Monthly Returns")

    # =================================================
    # 26 & 27: MA Crossover + Buy/Sell Signals
    # =================================================
    st.subheader("Moving Average Crossover & Buy/Sell Signals")

    c1, c2 = st.columns(2)

    for crypto, df, col in [("Bitcoin", btc, c1), ("Ethereum", eth, c2)]:
        with col:
            ma_df = df.dropna(subset=["MA_7", "MA_30"])

            if has_enough_data(ma_df):
                fig, ax = plt.subplots()
                ax.plot(ma_df.index, ma_df["Close"], label="Price")
                ax.plot(ma_df.index, ma_df["MA_7"], label="MA 7")
                ax.plot(ma_df.index, ma_df["MA_30"], label="MA 30")

                buy = ma_df[ma_df["MA_7"] > ma_df["MA_30"]]
                sell = ma_df[ma_df["MA_7"] < ma_df["MA_30"]]

                ax.scatter(buy.index, buy["Close"], marker="^", label="Buy")
                ax.scatter(sell.index, sell["Close"], marker="v", label="Sell")

                ax.set_title(f"{crypto} Buy/Sell Signals")
                ax.legend()
                st.pyplot(fig)

    # =================================================
    # 28: KPI Cards (BTC vs ETH)
    # =================================================
    st.subheader("Key Performance Indicators")

    btc_kpi = calculate_kpis(btc)
    eth_kpi = calculate_kpis(eth)

    k1, k2 = st.columns(2)

    with k1:
        st.markdown("### 🟦 Bitcoin")
        st.metric("ROI (%)", f"{btc_kpi[0]:.2f}")
        st.metric("Volatility (%)", f"{btc_kpi[1]:.2f}")
        st.metric("Max Drawdown (%)", f"{btc_kpi[2]:.2f}")

    with k2:
        st.markdown("### 🟧 Ethereum")
        st.metric("ROI (%)", f"{eth_kpi[0]:.2f}")
        st.metric("Volatility (%)", f"{eth_kpi[1]:.2f}")
        st.metric("Max Drawdown (%)", f"{eth_kpi[2]:.2f}")

    # =================================================
    # 29: Correlation Matrix
    # =================================================
    st.subheader("BTC vs ETH Correlation Matrix")

    merged = pd.concat(
        [btc["Returns"], eth["Returns"]],
        axis=1,
        keys=["BTC", "ETH"]
    ).dropna()

    if has_enough_data(merged):
        fig, ax = plt.subplots()
        sns.heatmap(merged.corr(), annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Return Correlation")
        st.pyplot(fig)

    # =================================================
    # 30: Executive Summary
    # =================================================
    st.subheader("📌Executive Summary Insights")

    better = "Bitcoin" if btc_kpi[0] > eth_kpi[0] else "Ethereum"
    riskier = "Ethereum" if eth_kpi[1] > btc_kpi[1] else "Bitcoin"

    st.success(
        f"""
        • **{better}** delivered higher overall returns in the selected period.  
        • **{riskier}** exhibits higher volatility and risk exposure.  
        • Trend-following signals are visible for both assets.  
        • High correlation indicates limited diversification within crypto portfolios.
        """
    )
