import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from data.newsfetcher import fetch_news


# -------------------------------------------------
# Utility
# -------------------------------------------------
def analyze_sentiment(headlines):
    analyzer = SentimentIntensityAnalyzer()
    return [analyzer.polarity_scores(h)["compound"] for h in headlines]


# -------------------------------------------------
# Main Render Function
# -------------------------------------------------
def render():
    st.title("🧠 NLP-Based Sentiment Analysis (News)")

    crypto = st.selectbox("Select Cryptocurrency", ["Bitcoin", "Ethereum"])

    news_df = fetch_news(crypto, limit=25)

    if news_df.empty:
        st.warning("No news data available.")
        return

    # Sentiment scores
    news_df["sentiment_score"] = analyze_sentiment(news_df["headline"])

    # Sentiment labels
    news_df["sentiment"] = news_df["sentiment_score"].apply(
        lambda x: "Positive" if x > 0.05 else "Negative" if x < -0.05 else "Neutral"
    )

    # =================================================
    # Chart 31: Sentiment Distribution
    # =================================================
    st.subheader("Sentiment Distribution")

    sentiment_counts = news_df["sentiment"].value_counts()

    fig, ax = plt.subplots()
    sentiment_counts.plot(kind="bar", ax=ax)
    ax.set_ylabel("Number of Headlines")
    ax.set_title(f"{crypto} News Sentiment Distribution")
    st.pyplot(fig)

    # =================================================
    # Chart 32: Sentiment Score Trend
    # =================================================
    st.subheader("Headline-wise Sentiment Scores")

    fig, ax = plt.subplots()
    ax.plot(news_df["sentiment_score"].values, marker="o")
    ax.axhline(0, linestyle="--", color="black")
    ax.set_ylabel("Sentiment Score")
    ax.set_title("Sentiment Polarity per Headline")
    st.pyplot(fig)

    # =================================================
    # Insights
    # =================================================
    st.subheader("📌 Sentiment Insights")

    avg_sentiment = news_df["sentiment_score"].mean()

    if avg_sentiment > 0.05:
        st.success("Overall market sentiment is **POSITIVE 📈**")
    elif avg_sentiment < -0.05:
        st.error("Overall market sentiment is **NEGATIVE 📉**")
    else:
        st.info("Overall market sentiment is **NEUTRAL ⚖️**")

    st.markdown("### 📰 Recent Headlines")
    for _, row in news_df.head(5).iterrows():
        st.write(f"• **{row['headline']}**")
        st.caption(f"{row['source']} | {row['published']}")
