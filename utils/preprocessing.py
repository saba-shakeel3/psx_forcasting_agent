# utils/preprocessing.py
import pandas as pd
import numpy as np

def clean_merged_data(df):
    # Forward-fill stock prices
    df['Close'] = df['Close'].fillna(method='ffill')

    # Drop rows with missing sentiment scores
    df.dropna(subset=['sentiment_score'], inplace=True)

    # Drop unnecessary columns
    df = df[['timestamp', 'Close', 'Volume', 'title', 'sentiment_score']]
    
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/merged_data.csv")
    df = clean_merged_data(df)
    df.to_csv("data/cleaned_data.csv", index=False)
