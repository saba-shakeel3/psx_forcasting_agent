# psx_agent_ai/main.py
from fastapi import FastAPI
import pandas as pd

# Import pipeline modules
from agents.stock_collector import fetch_stock_data
from agents.news_collector import fetch_news
from agents.sentiment_analyzer import analyze_sentiment
from agents.data_merger import merge_data as merge_stock_and_news
from utils.preprocessing import clean_merged_data
from forecast.forecast_lstm import forecast_next_price

app = FastAPI(title="PSX News Forecasting API")

# ------------------------
# Home Route
# ------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to the PSX News Forecasting API. Visit /docs to explore the available endpoints."
    }

# ------------------------
# Pipeline Runner
# ------------------------
@app.get("/run-pipeline")
def run_pipeline():
    # 1. Fetch stock data
    stock_df = fetch_stock_data()
    if stock_df is None:
        return {"error": "Failed to fetch stock data"}
    stock_df.to_csv("data/stock_data.csv", index=False)

    # 2. Fetch news data
    news_df = fetch_news()
    news_df.to_csv("data/news_data.csv", index=False)

    # 3. Sentiment analysis
    news_df = analyze_sentiment(news_df)
    news_df.to_csv("data/news_with_sentiment.csv", index=False)

    # 4. Merge stock & news
    merged_df = merge_stock_and_news("data/stock_data.csv", "data/news_with_sentiment.csv")
    merged_df.to_csv("data/merged_data.csv", index=False)

    return {"status": "Pipeline completed", "records_processed": len(merged_df)}

# ------------------------
# Get Latest Data
# ------------------------
@app.get("/get-latest")
def get_latest():
    df = pd.read_csv("data/merged_data.csv")
    return df.tail(5).to_dict(orient="records")

# ------------------------
# Forecast Endpoint
# ------------------------
@app.get("/forecast")
def get_forecast():
    predicted_price = forecast_next_price()

    # Convert numpy.float32 to regular Python float
    return {"predicted_next_closing_price": float(predicted_price)}


# ------------------------
# Run the API
# ------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
#hello world
