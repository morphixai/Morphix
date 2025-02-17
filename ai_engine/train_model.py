import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv

# โหลดค่าตัวแปรจากไฟล์ .env
load_dotenv()

DATA_PATH = os.getenv("DATA_PATH", "data/market_data.csv")  # ใช้ dataset จากไฟล์ CSV
MODEL_PATH = os.getenv("MODEL_PATH", "models/lstm_model.h5")  # บันทึกโมเดล
EPOCHS = int(os.getenv("EPOCHS", 50))  # จำนวนรอบการฝึก
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))  # ขนาด batch

# โหลดข้อมูลตลาด
def load_market_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ Market data file not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    print(f"✅ Loaded market data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

# เตรียมข้อมูลสำหรับ LSTM
def preprocess_data(df, feature_col="Close", sequence_length=30):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[[feature_col]])

    X, y = [], []
    for i in range(len(scaled_data) - sequence_length):
        X.append(scaled_data[i:i + sequence_length])
        y.append(scaled_data[i + sequence_length])

    X, y = np.array(X), np.array(y)
    print(f"✅ Data prepared: X shape = {X.shape}, y shape = {y.shape}")
    return X, y, scaler

# สร้างโมเดล LSTM
def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=1)  # ทำนายราคาถัดไป
    ])

    model.compile(optimizer="adam", loss="mean_squared_error")
    print("✅ LSTM Model Created!")
    return model

# ฝึกโมเดลและบันทึกผล
def train_and_save_model(X_train, y_train, scaler):
    model = build_lstm_model((X_train.shape[1], X_train.shape[2]))
    
    model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE)
    model.save("models/lstm_model.keras")

    
    print(f"✅ Model Trained and Saved at {MODEL_PATH}")
    return model, scaler

if __name__ == "__main__":
    try:
        df = load_market_data()
        X, y, scaler = preprocess_data(df)
        model, scaler = train_and_save_model(X, y, scaler)
    except Exception as e:
        print(f"❌ Error: {e}")
