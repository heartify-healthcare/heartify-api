import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Dropout, Input
import joblib

# Đọc dữ liệu
df = pd.read_csv("./model/heart_statlog_cleveland_hungary_final.csv")

# Tách input (X) và label (y)
X = df.drop(columns=["cholesterol", "fasting blood sugar", "oldpeak", "ST slope", "target"]).values  # target là nhãn bệnh tim
y = df["target"].values

df.head
# Chuẩn hóa
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, "./model/scaler.save")
# Reshape thành (samples, timesteps, features)
X_reshaped = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))

# Tách train/test
X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y, test_size=0.2, random_state=42)


model = Sequential([
    Input(shape=(X_train.shape[1], X_train.shape[2])),  # Chính xác: (timesteps, features)
    Conv1D(filters=32, kernel_size=3, activation='relu'),
    MaxPooling1D(pool_size=2),
    LSTM(64, return_sequences=True), #add return_sequences=True to ensure the output is 3D
    LSTM(32), # Add another LSTM layer to process the sequence
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid') # Output layer for binary classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.1)

y_pred = model.predict(X_test)
y_pred_classes = (y_pred > 0.5).astype("int32")

print("Accuracy:", accuracy_score(y_test, y_pred_classes))
print("Classification Report:\n", classification_report(y_test, y_pred_classes))

model.save("./model/heart_cnn_lstm_model.keras")