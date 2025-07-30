# psx_agent_ai/agents/data_merger.py

import pandas as pd

def merge_data(stock_path="data/stock_data.csv", news_path="data/news_with_sentiment.csv"):
    """
    Merges stock and news data on the hourly timestamp.
    Cleans, fills missing values, and saves final CSV.
    """

    # Load datasets
    stock_df = pd.read_csv(stock_path, parse_dates=["Datetime"])
    news_df = pd.read_csv(news_path, parse_dates=["publishedAt"])

    # Remove malformed rows (e.g., with all text values)
    stock_df = stock_df[stock_df["Close"].apply(lambda x: str(x).replace(".", "", 1).isdigit())]

    # Floor timestamps to hour
    stock_df["hour"] = stock_df["Datetime"].dt.floor("h")
    news_df["hour"] = news_df["publishedAt"].dt.floor("h")

    # Convert sentiment to numeric (if not already)
    if "sentiment" in news_df.columns:
        news_df["sentiment_numeric"] = pd.to_numeric(news_df["sentiment"], errors="coerce")
    else:
        news_df["sentiment_numeric"] = 0.0

    # Group news by hour
    sentiment_hourly = news_df.groupby("hour")["sentiment_numeric"].mean().reset_index()

    # Merge on 'hour'
    merged_df = pd.merge(stock_df, sentiment_hourly, on="hour", how="left")

    # Fill missing sentiment with 0 (neutral)
    merged_df["sentiment_numeric"] = merged_df["sentiment_numeric"].fillna(0)

    # Drop any rows with missing essential stock values
    merged_df.dropna(subset=["Close", "Open", "High", "Low", "Volume"], inplace=True)

    # Save cleaned data
    merged_df.to_csv("data/merged_data.csv", index=False)
    print(f"[✔] Cleaned & Merged data saved to data/merged_data.csv with {len(merged_df)} rows.")

    return merged_df

if __name__ == "__main__":
    merge_data()
