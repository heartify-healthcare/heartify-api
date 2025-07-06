import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, accuracy_score, 
    precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv1D, MaxPooling1D, LSTM, 
    Dense, Dropout, Input, BatchNormalization
)
from tensorflow.keras.regularizers import l2
import joblib
import time
from timeit import default_timer as timer

# Đọc dữ liệu
df = pd.read_csv("./model/heart_statlog_cleveland_hungary_final.csv")

# Tách input (X) và label (y)
X = df.drop(columns=["target"]).values
y = df["target"].values

# Chuẩn hóa
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, "./model/scaler.save")

# Reshape thành (samples, timesteps, features)
X_reshaped = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))

# Tách train/test
X_train, X_test, y_train, y_test = train_test_split(
    X_reshaped, y, test_size=0.2, random_state=42, stratify=y
)

# Xây dựng model
model = Sequential([
    Input(shape=(X_train.shape[1], X_train.shape[2])),
    
    Conv1D(filters=48, kernel_size=3, activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),
    
    LSTM(80, return_sequences=True, recurrent_dropout=0.2),
    BatchNormalization(),
    
    LSTM(40, recurrent_dropout=0.2),
    BatchNormalization(),
    
    Dense(80, activation='relu', kernel_regularizer=l2(0.001)),
    Dropout(0.4),
    
    Dense(1, activation='sigmoid')
])

# Compile model
optimizer = tf.keras.optimizers.Adam(learning_rate=0.0008)
model.compile(
    optimizer=optimizer,
    loss='binary_crossentropy',
    metrics=[
        'accuracy',
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall'),
        tf.keras.metrics.AUC(name='auc')
    ]
)

# Callbacks
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=8, monitor='val_auc', mode='max'),
    tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=4)
]

# Huấn luyện model
start_train = timer()
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.1,
    callbacks=callbacks,
    verbose=1
)
train_time = timer() - start_train

# Đánh giá model
start_inference = timer()
y_pred = model.predict(X_test)
inference_time = timer() - start_inference
inference_time_per_sample = inference_time / len(X_test)

y_pred_classes = (y_pred > 0.5).astype("int32")

# Tính toán các metrics
accuracy = accuracy_score(y_test, y_pred_classes)
precision = precision_score(y_test, y_pred_classes)
recall = recall_score(y_test, y_pred_classes)
f1 = f1_score(y_test, y_pred_classes)
roc_auc = roc_auc_score(y_test, y_pred)

# Tính specificity từ confusion matrix
tn, fp, fn, tp = confusion_matrix(y_test, y_pred_classes).ravel()
specificity = tn / (tn + fp)

# In kết quả đánh giá
print("\n=== Kết quả đánh giá ===")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall/Sensitivity: {recall:.4f}")
print(f"Specificity: {specificity:.4f}")
print(f"F1-score: {f1:.4f}")
print(f"AUC-ROC: {roc_auc:.4f}")
print(f"Thời gian huấn luyện: {train_time:.2f} giây")
print(f"Thời gian dự đoán trung bình mỗi mẫu: {inference_time_per_sample*1000:.4f} ms")

print("\nClassification Report:")
print(classification_report(y_test, y_pred_classes))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred_classes))

# Lưu model
model.save("./model/heart_cnn_lstm_model.keras")