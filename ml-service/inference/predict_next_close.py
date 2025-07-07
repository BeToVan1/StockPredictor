import numpy as np
import pandas as pd
import yfinance as yf
import keras
from sklearn.preprocessing import MinMaxScaler
import pickle

def predict_next_close(ticker, window_size):
    # load model
    model = keras.models.load_model(f"../models/lstm_model_{ticker}_day.keras")

    # Fetch data (ensures at least window size)
    df = yf.download(ticker, period=f"{window_size + 10}d", interval="1d")
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA10"] = df["Close"].rolling(10).mean()
    df = df.dropna()

    features = df[["Close", "MA5", "MA10"]]

    with open(f"../models/scaler_{ticker}.pkl", "rb") as f:
        scaler = pickle.load(f)

    scaled = scaler.transform(features)
    last_window = scaled[-window_size:]
    last_window = last_window.reshape((1, window_size, 3))

    model = keras.models.load_model(f"../models/lstm_model_{ticker}_day.keras")

    # Make prediction
    pred_scaled = model.predict(last_window)[0][0]

    # Inverse transform to get actual predicted close price
    pred_scaled_vector = np.array([[pred_scaled, 0, 0]])  # padding dummy values for MA5 and MA10
    pred_actual = scaler.inverse_transform(pred_scaled_vector)[0][0]  # only use the 'Close' column

    print(f"📈 Predicted next close for {ticker}: ${pred_actual:.2f}")
    return pred_actual

if __name__ == "__main__":
    predict_next_close('TGT', 60)