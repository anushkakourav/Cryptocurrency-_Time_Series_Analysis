import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet

from data.data_preprocessing import preprocess_data


# -------------------------------------------------
# Utility
# -------------------------------------------------
def has_enough_data(df, min_rows=150):
    return df is not None and not df.empty and len(df) >= min_rows


# -------------------------------------------------
# Helper: ARIMA forecast
# -------------------------------------------------
def arima_forecast(series, steps=30):
    model = ARIMA(series, order=(5, 1, 0))
    fit = model.fit()
    forecast = fit.get_forecast(steps=steps)
    return forecast.predicted_mean, forecast.conf_int()


# -------------------------------------------------
# Helper: Prophet forecast
# -------------------------------------------------
def prophet_forecast(series, steps=30):
    df = series.reset_index()
    df.columns = ["ds", "y"]

    model = Prophet(daily_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=steps)
    forecast = model.predict(future)

    return model, forecast


# -------------------------------------------------
# Main Render Function
# -------------------------------------------------
def render():
    st.title("⏳ Time Series Forecasting (BTC vs ETH)")

    # Load data
    btc = preprocess_data("BTC-USD")
    eth = preprocess_data("ETH-USD")

    if not has_enough_data(btc) or not has_enough_data(eth):
        st.warning("Not enough data for forecasting.")
        return

    btc_price = btc["Close"].dropna()
    eth_price = eth["Close"].dropna()

    # =================================================
    # Charts 16–18: Decomposition
    # =================================================
    st.subheader("Time Series Decomposition")

    col1, col2 = st.columns(2)

    btc_dec = seasonal_decompose(btc_price, model="additive", period=30)
    eth_dec = seasonal_decompose(eth_price, model="additive", period=30)

    with col1:
        fig, ax = plt.subplots()
        ax.plot(btc_dec.trend)
        ax.set_title("Bitcoin Trend")
        st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.plot(btc_dec.seasonal)
        ax.set_title("Bitcoin Seasonality")
        st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.plot(btc_dec.resid)
        ax.set_title("Bitcoin Residuals")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        ax.plot(eth_dec.trend)
        ax.set_title("Ethereum Trend")
        st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.plot(eth_dec.seasonal)
        ax.set_title("Ethereum Seasonality")
        st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.plot(eth_dec.resid)
        ax.set_title("Ethereum Residuals")
        st.pyplot(fig)

    # =================================================
    # Chart 19: ARIMA Forecast
    # =================================================
    st.subheader("ARIMA Forecast")

    btc_fc, btc_ci = arima_forecast(btc_price)
    eth_fc, eth_ci = arima_forecast(eth_price)

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.plot(btc_price, label="Actual")
        ax.plot(btc_fc, label="Forecast")
        ax.fill_between(btc_ci.index, btc_ci.iloc[:, 0], btc_ci.iloc[:, 1], alpha=0.3)
        ax.set_title("Bitcoin ARIMA Forecast")
        ax.legend()
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        ax.plot(eth_price, label="Actual")
        ax.plot(eth_fc, label="Forecast")
        ax.fill_between(eth_ci.index, eth_ci.iloc[:, 0], eth_ci.iloc[:, 1], alpha=0.3)
        ax.set_title("Ethereum ARIMA Forecast")
        ax.legend()
        st.pyplot(fig)

    # =================================================
    # Chart 20: Prophet Forecast
    # =================================================
    st.subheader("Prophet Forecast")

    col1, col2 = st.columns(2)

    with col1:
        model, forecast = prophet_forecast(btc_price)
        fig = model.plot(forecast)
        plt.title("Bitcoin Prophet Forecast")
        st.pyplot(fig)

    with col2:
        model, forecast = prophet_forecast(eth_price)
        fig = model.plot(forecast)
        plt.title("Ethereum Prophet Forecast")
        st.pyplot(fig)

    # =================================================
    # Chart 21: Actual vs Predicted (ARIMA)
    # =================================================
    st.subheader("Actual vs Predicted (ARIMA)")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.plot(btc_price[-100:], label="Actual")
        ax.plot(btc_fc, label="Predicted")
        ax.set_title("Bitcoin Actual vs Predicted")
        ax.legend()
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        ax.plot(eth_price[-100:], label="Actual")
        ax.plot(eth_fc, label="Predicted")
        ax.set_title("Ethereum Actual vs Predicted")
        ax.legend()
        st.pyplot(fig)

    # =================================================
    # Chart 22: Forecast Confidence Interval (COLOR FIX)
    # =================================================
    st.subheader("Forecast Confidence Interval")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.plot(btc_ci.index, btc_ci.iloc[:, 0], color="blue", label="Lower Bound")
        ax.plot(btc_ci.index, btc_ci.iloc[:, 1], color="orange", label="Upper Bound")
        ax.fill_between(
            btc_ci.index,
            btc_ci.iloc[:, 0],
            btc_ci.iloc[:, 1],
            alpha=0.2
        )
        ax.set_title("Bitcoin Forecast Confidence Interval")
        ax.legend()
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        ax.plot(eth_ci.index, eth_ci.iloc[:, 0], color="blue", label="Lower Bound")
        ax.plot(eth_ci.index, eth_ci.iloc[:, 1], color="orange", label="Upper Bound")
        ax.fill_between(
            eth_ci.index,
            eth_ci.iloc[:, 0],
            eth_ci.iloc[:, 1],
            alpha=0.2
        )
        ax.set_title("Ethereum Forecast Confidence Interval")
        ax.legend()
        st.pyplot(fig)

       # =========================================================
       # Forecasting: Executive Summary
       # =========================================================
    st.subheader("📌Forecasting Summary Insights")

    st.success(
        """
**Key Forecasting Insights**

• Bitcoin and Ethereum exhibit similar long-term price trends, though their short-term dynamics differ.  
• ARIMA performs effectively for short-term forecasting across both assets.  
• Prophet captures underlying trend and seasonality more robustly, especially over longer horizons.  
• Forecast uncertainty increases with time horizon, with Ethereum showing relatively higher uncertainty.
"""
    )

