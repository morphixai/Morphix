import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

# โหลดโมเดล
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/lstm_model.h5")
model = load_model(MODEL_PATH)

# โหลดข้อมูลตลาด
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/market_data.csv")

try:
    df = pd.read_csv(DATA_PATH)
    print(f"✅ Loaded market data: {df.shape[0]} rows, {df.shape[1]} columns")
except FileNotFoundError:
    print(f"❌ Error: Market data file not found: {DATA_PATH}")
    exit()

# ใช้ข้อมูล 30 วันสุดท้ายในการพยากรณ์
scaler = MinMaxScaler(feature_range=(0, 1))
data = df["Close"].values.reshape(-1, 1)
scaled_data = scaler.fit_transform(data)

sequence_length = 30
input_data = scaled_data[-sequence_length:].reshape(1, sequence_length, 1)

# พยากรณ์ราคา
predicted_price = model.predict(input_data)
predicted_price = scaler.inverse_transform(predicted_price)

print(f"📈 Predicted Price: {predicted_price[0][0]:.2f} USDT")
