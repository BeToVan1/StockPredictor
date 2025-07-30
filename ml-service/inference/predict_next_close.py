import numpy as np
import pandas as pd
import yfinance as yf
import keras
import pickle
import sys
import json
import os
import time
from train_model import train

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def predict_future_close(ticker, window_size, days_ahead):
    model_path = f"../ml-service/models/lstm_model_{ticker}_day.keras"
    scaler_path = f"../ml-service/models/scaler_{ticker}.pkl"

    #Train model if not present
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        train(ticker, '2y', '1d', 60)

    # Load model and scaler
    model = keras.models.load_model(model_path)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    # Fetch recent closing prices (extra days in case of market closures)
    df = yf.download(ticker, period=f"{window_size + 10}d", interval="1d")
    df = df.dropna()
    close_prices = df["Close"].values.reshape(-1, 1)

    # Scale and create the last window
    scaled = scaler.transform(close_prices)
    last_window = scaled[-window_size:].reshape(1, window_size, 1)

    # Predict iteratively
    for _ in range(days_ahead):
        next_scaled = model.predict(last_window, verbose=0)[0][0]  # Predict next day
        next_scaled = np.array([next_scaled])  # Reshape for stacking
        # Slide window: remove first, append new prediction
        last_window = np.append(last_window[:, 1:, :], [[next_scaled]], axis=1)

    # Inverse scale the final prediction
    future_price = scaler.inverse_transform([next_scaled])[0][0]
    # print(f"Predicted close in {days_ahead} trading days for {ticker}: ${future_price:.2f}")
    return future_price

if __name__ == "__main__":
    ticker = sys.argv[1]
    window_size = int(sys.argv[2])
    days_ahead = int(sys.argv[3])

    prediction = predict_future_close(ticker, window_size, days_ahead)
    print(json.dumps({"ticker": ticker, "prediction" : float(prediction)}))
   