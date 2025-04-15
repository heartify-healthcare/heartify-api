# 🫀 Cardiovascular Disease Prediction API

This is a Flask-based REST API that deploys a trained **CNN + LSTM model** to predict the likelihood of cardiovascular disease. The deep learning model is trained using Python and TensorFlow on **Google Colab** or **Kaggle**, and exported as a `.keras` file for deployment.

## 💡 Features

- ✅ RESTful API using Flask
- ✅ Loads a trained CNN+LSTM model
- ✅ Accepts patient data via JSON POST requests
- ✅ Returns predictions in real-time
- ✅ Simple and easy to integrate into any front-end or mobile app

## 🧠 Model Overview

- Architecture: **CNN + LSTM**
- Framework: **TensorFlow/Keras**
- Training environment: **Google Colab / Kaggle**
- Model output: `.keras` format

The model is trained on a dataset of patient health records including attributes such as:
- Age
- Gender
- Resting Blood Pressure
- Cholesterol levels
- Chest pain type
- Maximum heart rate
- ...and other cardiovascular-related features

## 📦 Project Structure

