"""
Service layer for the prediction module.
This layer contains the business logic for the prediction module.
"""
from typing import Dict, Any, List, Union
from app.prediction.interface import PredictionInterface
from app.prediction.schema import HeartDiseaseInput

class PredictionService:
    """Service for heart disease prediction."""
    
    @staticmethod
    def predict_heart_disease(input_data: HeartDiseaseInput) -> Dict[str, Any]:
        """
        Predict heart disease based on input data.
        
        Args:
            input_data: Validated input data
            
        Returns:
            Dictionary containing prediction results
        """
        # Convert pydantic model to list of features in the correct order
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
        
        # Make prediction using the interface
        result = PredictionInterface.predict(features)
        
        return result