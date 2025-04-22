import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load model đã huấn luyện
model = load_model("/content/heart_cnn_lstm_model.keras")

# Load scaler đã được fit trên dữ liệu train
scaler = joblib.load("/content/scaler.save")

# Dữ liệu mẫu (phải đúng thứ tự cột như trong dataset gốc)
X = np.array([[52,1,4,160,246,0,1,82,1,4.0,2]])

# Chuẩn hóa
X_scaled = scaler.transform(X)

# Reshape
X_reshaped = X_scaled.reshape((1, X.shape[1], 1))

# Dự đoán
prediction = model.predict(X_reshaped)
predicted_class = (prediction > 0.5).astype("int32")

print("Xác suất bị bệnh tim:", prediction[0][0])
print("Kết luận:", "CÓ BỆNH" if predicted_class[0][0] == 1 else "KHÔNG BỆNH")