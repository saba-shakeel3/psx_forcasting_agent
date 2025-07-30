# psx_agent_ai/agents/sentiment_analyzer.py
from transformers import pipeline
import pandas as pd

sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", revision="714eb0f")


def analyze_sentiment(news_df):
    sentiment_model = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    
    news_df['sentiment'] = news_df['title'].apply(lambda x: sentiment_model(x)[0]['label'])
    
    return news_df


if __name__ == "__main__":
    df = pd.read_csv("data/news_data.csv")
    df = analyze_sentiment(df)
    df.to_csv("data/news_with_sentiment.csv", index=False)