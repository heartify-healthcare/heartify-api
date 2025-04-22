# Cardiovascular Disease Detection API (Flask)

This repository contains the **Flask-based REST API** component of a university capstone project. The API serves as a backend for receiving health metrics from a mobile application and uses a deep learning model (CNN + LSTM) to predict the likelihood of **cardiovascular disease (CVD)**.

## 🧠 How It Works

1. The mobile app sends user health data (e.g., age, blood pressure, cholesterol) to the backend via HTTP POST.
2. The API preprocesses the input and feeds it into a trained deep learning model (`.keras` format).
3. The model returns a binary prediction indicating potential CVD risk.
4. The API responds with the result to the mobile app.

## 🛠️ Technologies Used

- **Python 3.10+**
- **Flask** — Lightweight web framework for Python
- **TensorFlow / Keras** — For loading and running the deep learning model
- **Flask-CORS** — Handles cross-origin requests from the mobile app
- **Gunicorn / WSGI (optional)** — For production-ready deployment

## 🧪 Input Example

Health metrics expected (in JSON format):

```json
{
  "age": 18,
  "sex": 1,
  "cp": 4,
  "trestbps": 80,
  "chol": 246,
  "fbs": 0,
  "restecg": 1,
  "thalach": 82,
  "exang": 1,
  "oldpeak": 4.0,
  "slope": 2
}
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- `pip`

### Installation

```bash
git clone https://github.com/votranphi/flask-cardiovascular-disease
cd flask-cardiovascular-disease
pip install -r requirements.txt
```

### Train the CNN-LSTM model

```bash
python model/train.py
```

Make sure the trained `.keras` model and the `scaler.save` file is placed in the appropriate directory (usually `model`) after completing the training progress.

### Running the Server

```bash
python manage.py run
```

The API will be available at:  
`http://127.0.0.1:5000/api/prediction/heart-disease`

### Sample Prediction Request (with `curl`)

```bash
curl -X POST http://127.0.0.1:5000/api/prediction/heart-disease \
     -H "Content-Type: application/json" \
     -d @sample_data.json
```

## 🧠 Model

- Architecture: **CNN + LSTM hybrid model**
- Trained on a cardiovascular dataset with preprocessed and normalized input features
- Sample output: `{ "prediction": "POSITIVE", "probability": 0.9983527064323425 }`

## 🔗 Frontend Integration

This API is used by the mobile frontend built with React Native & Expo.  
👉 Mobile App Repository: [https://github.com/votranphi/react-native-cardiovascular-disease](https://github.com/votranphi/react-native-cardiovascular-disease)

## 📚 Academic Context

This API is part of a university **capstone project** (not a graduation thesis), developed under the topic:

> **"Deep learning-based AIoT system for cardiovascular disease prediction: A CNN-LSTM approach."**

## ✍️ Authors

- [Vo Tran Phi](https://github.com/votranphi)
- [Le Duong Minh Phuc](https://github.com/minhphuc2544)

## 📄 License

This project is for academic purposes only. It is not intended for clinical or commercial use.