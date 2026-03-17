import pandas as pd
import feedparser

# Google News RSS URLs (crypto-specific)
GOOGLE_NEWS_RSS = {
    "Bitcoin": "https://news.google.com/rss/search?q=bitcoin+cryptocurrency&hl=en-IN&gl=IN&ceid=IN:en",
    "Ethereum": "https://news.google.com/rss/search?q=ethereum+cryptocurrency&hl=en-IN&gl=IN&ceid=IN:en",
}


def fetch_news(crypto="Bitcoin", limit=20):
    """
    Fetch latest crypto-related news headlines using Google News RSS
    """
    url = GOOGLE_NEWS_RSS.get(crypto)
    if not url:
        return pd.DataFrame()

    feed = feedparser.parse(url)

    data = []
    for entry in feed.entries[:limit]:
        data.append({
            "headline": entry.title,
            "published": entry.published,
            "source": entry.source.title if "source" in entry else "Google News"
        })

    return pd.DataFrame(data)
