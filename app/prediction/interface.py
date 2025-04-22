"""
Interface layer for the prediction module.
This layer handles the interaction with the model.
"""
from typing import Dict, Any, List, Tuple, Union
from app.prediction.model import HeartDiseaseModel

class PredictionInterface:
    """Interface for the heart disease prediction model."""
    
    @staticmethod
    def predict(features: List[Union[int, float]]) -> Dict[str, Any]:
        """
        Make a prediction using the heart disease model.
        
        Args:
            features: List of input features
            
        Returns:
            Dictionary containing prediction results
        """
        model = HeartDiseaseModel()
        probability, prediction = model.predict(features)
        
        return {
            "probability": probability,
            "prediction": prediction
        }