import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from data.data_preprocessing import preprocess_data

sns.set_style("darkgrid")


# -------------------------------------------------
# Utility
# -------------------------------------------------
def has_enough_data(df, min_rows=50):
    return df is not None and not df.empty and len(df) >= min_rows


# -------------------------------------------------
# Main Render Function
# -------------------------------------------------
def render():
    st.title("📊 Exploratory Data Analysis (EDA)")

    # Load processed data
    btc = preprocess_data("BTC-USD")
    eth = preprocess_data("ETH-USD")

    # =================================================
    # Chart 1 & 2: Price Trend (Side-by-Side)
    # =================================================
    st.subheader("Price Trend Comparison")

    if has_enough_data(btc) and has_enough_data(eth):
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.plot(btc.index, btc["Close"])
            ax.set_title("Bitcoin Price Trend")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            ax.plot(eth.index, eth["Close"], color="orange")
            ax.set_title("Ethereum Price Trend")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            st.pyplot(fig)

    # =================================================
    # Chart 3 & 4: Trading Volume (Side-by-Side)
    # =================================================
    st.subheader("Trading Volume Comparison")

    if has_enough_data(btc) and has_enough_data(eth):
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.plot(btc.index, btc["Volume"])
            ax.set_title("Bitcoin Trading Volume")
            ax.set_xlabel("Date")
            ax.set_ylabel("Volume")
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            ax.plot(eth.index, eth["Volume"], color="orange")
            ax.set_title("Ethereum Trading Volume")
            ax.set_xlabel("Date")
            ax.set_ylabel("Volume")
            st.pyplot(fig)

    # =================================================
    # Chart 5: Market Strength Comparison (NORMALIZED)
    # =================================================
    st.subheader("Market Strength Comparison (Normalized Prices)")

    if has_enough_data(btc) and has_enough_data(eth):
        btc_norm = btc["Close"] / btc["Close"].iloc[0]
        eth_norm = eth["Close"] / eth["Close"].iloc[0]

        fig, ax = plt.subplots()
        ax.plot(btc.index, btc_norm, label="Bitcoin (Normalized)")
        ax.plot(eth.index, eth_norm, label="Ethereum (Normalized)")
        ax.set_title("BTC vs ETH Relative Price Growth")
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Price")
        ax.legend()
        st.pyplot(fig)

    # =================================================
    # Chart 6: Daily Returns (Side-by-Side)
    # =================================================
    st.subheader("Daily Returns Comparison")

    if has_enough_data(btc) and has_enough_data(eth):
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.plot(btc.index, btc["Returns"], color="green")
            ax.axhline(0, linestyle="--", color="black")
            ax.set_title("Bitcoin Daily Returns")
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            ax.plot(eth.index, eth["Returns"], color="green")
            ax.axhline(0, linestyle="--", color="black")
            ax.set_title("Ethereum Daily Returns")
            st.pyplot(fig)

    # =================================================
    # Chart 7: Log Returns (Side-by-Side)
    # =================================================
    st.subheader("Log Returns Comparison")

    if has_enough_data(btc) and has_enough_data(eth):
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.plot(btc.index, btc["Log_Returns"], color="purple")
            ax.axhline(0, linestyle="--", color="black")
            ax.set_title("Bitcoin Log Returns")
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            ax.plot(eth.index, eth["Log_Returns"], color="purple")
            ax.axhline(0, linestyle="--", color="black")
            ax.set_title("Ethereum Log Returns")
            st.pyplot(fig)

    # =================================================
    # Chart 8: Price Distribution (Side-by-Side)
    # =================================================
    st.subheader("Price Distribution Comparison")

    if has_enough_data(btc) and has_enough_data(eth):
        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            sns.histplot(btc["Close"], bins=50, kde=True, ax=ax)
            ax.set_title("Bitcoin Price Distribution")
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            sns.histplot(eth["Close"], bins=50, kde=True, ax=ax)
            ax.set_title("Ethereum Price Distribution")
            st.pyplot(fig)

        # =========================================================
        # EDA Summary Insights
        # =========================================================
        st.subheader("📌EDA Summary Insights")

        if has_enough_data(btc) and has_enough_data(eth):
            btc_avg = btc["Returns"].mean()
            eth_avg = eth["Returns"].mean()

            btc_vol = btc["Returns"].std()
            eth_vol = eth["Returns"].std()

            btc_trend = "Bullish 📈" if btc_avg > 0 else "Bearish 📉"
            eth_trend = "Bullish 📈" if eth_avg > 0 else "Bearish 📉"

            st.success(
                f"""
                **Key Observations**

                • **Bitcoin** exhibits a **{btc_trend}** return trend over the analyzed period.  
                • **Ethereum** exhibits a **{eth_trend}** return trend over the analyzed period.  

                • **Bitcoin** shows return volatility of **{btc_vol:.4f}**, reflecting its price fluctuations.  
                • **Ethereum** shows return volatility of **{eth_vol:.4f}**, indicating relative risk behavior.
                """
                        )
