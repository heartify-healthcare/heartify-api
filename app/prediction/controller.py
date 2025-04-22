from flask import Blueprint, request, jsonify
from pydantic import ValidationError
import numpy as np
import os

from app.prediction.schema import HeartDiseaseInputSchema, PredictionResponseSchema, ErrorResponseSchema
from app.prediction.service import HeartDiseasePredictionService

# Create blueprint for prediction routes
prediction_bp = Blueprint('prediction', __name__, url_prefix='/api/prediction')

# Initialize prediction service
# Adjust paths based on your deployment structure
MODEL_PATH = os.environ.get('MODEL_PATH', 'models/heart_cnn_lstm_model.keras')
SCALER_PATH = os.environ.get('SCALER_PATH', 'models/scaler.save')

prediction_service = HeartDiseasePredictionService(
    model_path=MODEL_PATH,
    scaler_path=SCALER_PATH
)

@prediction_bp.route('/', methods=['POST'])
def predict():
    """Endpoint for heart disease prediction."""
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            error_response = ErrorResponseSchema(
                error="No input data provided",
                details={"message": "Request body must contain valid JSON"}
            )
            return jsonify(error_response.dict()), 400
        
        # Validate input data using Pydantic schema
        input_data = HeartDiseaseInputSchema(**data)
        
        # Extract features in the correct order
        features = [
            input_data.age,
            input_data.sex,
            input_data.cp,
            input_data.trestbps,
            input_data.chol,
            input_data.fbs,
            input_data.restecg,
            input_data.thalach,
            input_data.exang,
            input_data.oldpeak,
            input_data.slope
        ]
        
        # Make prediction
        result = prediction_service.predict(features)
        
        # Create response using the schema
        response = PredictionResponseSchema(
            probability=result["probability"],
            prediction=result["prediction"]
        )
        
        return jsonify(response.dict()), 200
        
    except ValidationError as e:
        # Handle validation errors
        error_response = ErrorResponseSchema(
            error="Input validation error",
            details=e.errors()
        )
        return jsonify(error_response.dict()), 400
    except Exception as e:
        # Handle other errors
        error_response = ErrorResponseSchema(
            error="Prediction failed",
            details={"message": str(e)}
        )
        return jsonify(error_response.dict()), 500