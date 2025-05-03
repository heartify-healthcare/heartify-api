from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.prediction.schema import HeartDiseaseInput, PredictionResponse
from app.prediction.service import PredictionService

# Create a blueprint for prediction routes
prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/heart-disease', methods=['POST'])
def predict_heart_disease():
    try:
        # Parse and validate input data
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validate with Pydantic schema
        input_data = HeartDiseaseInput(**request_data)
        
        # Process prediction using service layer
        result = PredictionService.predict_heart_disease(input_data)
        
        # Validate response with Pydantic schema
        response_data = PredictionResponse(**result)
        
        return jsonify(response_data.dict()), 200
        
    except ValidationError as e:
        # Handle validation errors from Pydantic
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
    except Exception as e:
        # Handle other errors
        return jsonify({"error": str(e)}), 500