import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import pickle



# predict next days close
def fetch_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval)
    df["Target"] = df["Close"].shift(-1) 
    return df.dropna()

# 5 day and 10 day moving averages
def prepare_features(df):
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA10"] = df["Close"].rolling(10).mean()
    return df.dropna()

# convert time series to LSTM-friendly sequences
def create_sequences(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size, 0])  # Predict 'Close'
    return np.array(X), np.array(y)

# training a model to predict
def train(ticker, period, interval, window_size):
    df = fetch_data(ticker, period, interval)
    df = prepare_features(df)

    features = df[["Close", "MA5", "MA10"]]
    #print(features.head())
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(features)

    X,y = create_sequences(scaled, window_size)

    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = Sequential([
        LSTM(64, return_sequences=True),
        LSTM(32),
        Dense(1)
    ])

    model.compile(loss="mse", optimizer="adam")
    model.fit(X_train,y_train,epochs=20, batch_size=32,validation_split=0.2)
    # predict
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)

    # evaluate
    train_mse = mean_squared_error(y_train, train_preds)
    test_mse = mean_squared_error(y_test, test_preds)
    train_rmse = np.sqrt(train_mse)
    test_rmse = np.sqrt(test_mse)

    print(f"Train MSE: {train_mse:.4f}")
    print(f"Test MSE: {test_mse:.4f}")

    print(f"Train RMSE: {train_rmse:.4f}")
    print(f"Test RMSE: {test_rmse:.4f}")
    
    model.save(f"../models/lstm_model_{ticker}_day.keras")
    with open(f"../models/scaler_{ticker}.pkl", "wb") as f:
        pickle.dump(scaler, f)

if __name__ == "__main__":
    train('TGT', '2y', '1d', 60)
