# psx_agent_ai/forecast/forecast_lstm.py

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def create_dataset(data, time_step=3):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

def forecast_next_price():
    file_path = "data/merged_data.csv"
    
    if not os.path.exists(file_path):
        print("[✘] Merged data not found at:", file_path)
        return None

    df = pd.read_csv(file_path)

    if 'Close' not in df.columns:
        print("[✘] 'Close' column not found in merged data.")
        return None

    df['Close'] = df['Close'].ffill()  # Avoid deprecated method warning

    if df['Close'].isnull().any():
        print("[✘] Null values still present in 'Close' column after forward fill.")
        return None

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[['Close']].values)

    time_step = 3
    X, y = create_dataset(scaled_data, time_step)
    if len(X) == 0:
        print("[✘] Not enough data to create sequences.")
        return None

    X = X.reshape(X.shape[0], X.shape[1], 1)

    # LSTM Model
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(32))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, y, epochs=20, batch_size=1, verbose=0)

    # Forecast
    last_values = scaled_data[-time_step:].reshape(1, time_step, 1)
    predicted_scaled = model.predict(last_values, verbose=0)
    predicted_price = scaler.inverse_transform(predicted_scaled)[0][0]

    predicted_price = float(predicted_price)  # Ensure compatibility with FastAPI/JSON
    print(f"[✔] Forecasted next closing price: {predicted_price:.2f}")
    return predicted_price

# Optional: Run standalone
if __name__ == "__main__":
    forecast_next_price()
