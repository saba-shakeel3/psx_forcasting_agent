# psx_agent_ai/agents/news_collector.py
import requests
import pandas as pd
from datetime import datetime
import os

API_KEY = "eb4b3627e8cb46ce923b2466283aedc6"  # Replace with your NewsAPI key

def fetch_news(query="PSX", page_size=20):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize={page_size}&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Failed to fetch news:", response.status_code, response.text)
        return pd.DataFrame()

    articles = response.json().get('articles', [])
    
    if not articles:
        print("⚠️ No articles found.")
        return pd.DataFrame()

    df = pd.DataFrame([{
        "publishedAt": article.get("publishedAt"),
        "title": article.get("title"),
        "description": article.get("description"),
        "source": article.get("source", {}).get("name")
    } for article in articles if article.get("publishedAt")])

    df['hour'] = pd.to_datetime(df['publishedAt'], errors='coerce').dt.floor('h')
    return df

if __name__ == "__main__":
    df = fetch_news()
    
    if df.empty:
        print("❌ No data to save.")
    else:
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/news_data.csv", index=False)
        print(f"✅ Saved {len(df)} news articles to data/news_data.csv")
