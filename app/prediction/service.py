import os
import numpy as np
import joblib
from typing import Dict, Any, List
import tensorflow as tf
from tensorflow.keras.models import load_model

from app.prediction.interface import PredictionInterface

class HeartDiseasePredictionService(PredictionInterface):
    """Service for heart disease prediction using the trained CNN-LSTM model."""
    
    def __init__(self, model_path: str, scaler_path: str):
        """
        Initialize the prediction service by loading the model and scaler.
        
        Args:
            model_path: Path to the saved Keras model
            scaler_path: Path to the saved scaler
        """
        # Load the model and scaler
        self._model = load_model(model_path)
        self._scaler = joblib.load(scaler_path)
        
    def predict(self, features: List[float]) -> Dict[str, Any]:
        """
        Make a heart disease prediction based on input features.
        
        Args:
            features: List of features in the correct order for prediction
            
        Returns:
            Dictionary containing prediction probability and result
        """
        # Convert features to numpy array with correct shape for preprocessing
        X = np.array([features])
        
        # Scale the features
        X_scaled = self._scaler.transform(X)
        
        # Reshape for CNN-LSTM model (samples, timesteps, features)
        X_reshaped = X_scaled.reshape((1, X.shape[1], 1))
        
        # Make prediction
        prediction_prob = float(self._model.predict(X_reshaped)[0][0])
        
        # Determine prediction result
        prediction_result = "POSITIVE" if prediction_prob > 0.5 else "NEGATIVE"
        
        return {
            "probability": prediction_prob,
            "prediction": prediction_result
        }