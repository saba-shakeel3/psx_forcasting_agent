import yfinance as yf
import pandas as pd
import datetime
import os

def fetch_stock_data(ticker="HBL.KA", start_date="2024-07-01", end_date=None, interval='1h'):
    # Ensure end date is today if not provided
    if end_date is None:
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Make sure the data directory exists
    os.makedirs("data", exist_ok=True)

    try:
        print(f"[•] Fetching stock data for {ticker} from {start_date} to {end_date}...")
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)

        if data.empty:
            print(f"[✘] No data fetched for {ticker}. Check the ticker symbol or internet connection.")
            return None

        data.reset_index(inplace=True)
        data['Ticker'] = ticker
        data.to_csv("data/stock_data.csv", index=False)

        print(f"[✔] Stock data saved to data/stock_data.csv")
        return data  # ✅ Return the DataFrame

    except Exception as e:
        print(f"[✘] Error fetching stock data: {e}")
        return None  # ✅ Make sure to return None on error

# For running directly
if __name__ == "__main__":
    fetch_stock_data("HBL.KA")
