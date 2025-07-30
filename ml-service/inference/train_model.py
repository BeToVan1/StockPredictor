import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.metrics import RootMeanSquaredError
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# predict next days close
def fetch_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval)
    return df.dropna()

# training a model to predict
def train(ticker, period, interval, window_size):
    df = fetch_data(ticker, period, interval)
    df = df.reset_index()
    stock_close = df["Close"]
    dataset = stock_close.values # convert to numpy array
    training_data_len = int(np.ceil(len(dataset) * 0.95)) # get 95% of data for training
    #print(df.head())
   
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(dataset)

    training_data = scaled_data[:training_data_len]

    X_train, y_train = [], []

    # Create sliding window for stock (60 days)
    for i in range(window_size, len(training_data)):
        X_train.append(training_data[i-window_size:i,0])
        y_train.append(training_data[i,0])
    
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    model = Sequential()

    # First Layer
    model.add(LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    # Second Layer
    model.add(LSTM(64, return_sequences=False))
    # Third Layer (Dense)
    model.add(Dense(128, activation="relu"))
    # Fourth Layer (Dropout)
    model.add(Dropout(0.5))
    # Final Output Layer
    model.add(Dense(1))

    model.compile(optimizer="adam", loss="mse", metrics=[RootMeanSquaredError()])

    model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)

    # Prep the test data
    test_data = scaled_data[training_data_len - 60:]
    X_test, y_test = [], dataset[training_data_len:]

    for i in range(60, len(test_data)):
        X_test.append(test_data[i-60:i, 0])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Make predictions
    test_preds = model.predict(X_test, verbose=0)
    test_preds = scaler.inverse_transform(test_preds)

    #Plot
    '''
    train = df[:training_data_len]
    test = df[training_data_len:]
    test = test.copy()
    test['Predictions'] = test_preds
    df['Date'] = pd.to_datetime(df['Date'])
    plt.figure(figsize=(12,8))
    plt.plot(train['Date'], train['Close'], label="Train (Actual)", color='blue')
    plt.plot(test['Date'], test['Close'], label="Test (Actual)", color='orange')
    plt.plot(test['Date'], test['Predictions'], label="Predictions", color='red')
    plt.title("Stock predictions")
    plt.xlabel("date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.show()
    # evaluate
    
    train_mse = mean_squared_error(y_train, train_preds)
    test_mse = mean_squared_error(y_test, test_preds)
    train_rmse = np.sqrt(train_mse)
    test_rmse = np.sqrt(test_mse)
    
    print(f"Train MSE: {train_mse:.4f}")
    print(f"Test MSE: {test_mse:.4f}")

    print(f"Train RMSE: {train_rmse:.4f}")
    print(f"Test RMSE: {test_rmse:.4f}")
    '''
    model.save(f"../ml-service/models/lstm_model_{ticker}_day.keras")
    with open(f"../ml-service/models/scaler_{ticker}.pkl", "wb") as f:
        pickle.dump(scaler, f)

if __name__ == "__main__":
    train('AMD', '2y', '1d', 60)
