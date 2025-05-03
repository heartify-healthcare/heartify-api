from sqlalchemy.orm import Session
from typing import Dict, Any, List, Union, Tuple, Optional
from app.prediction.schema import HeartDiseaseInput
from app.prediction.model import HeartDiseaseModel
from app.prediction.entity import Prediction
from app.prediction.repository import PredictionRepository
from app.users.repository import UserRepository

class PredictionService:
    def __init__(self, db: Session):
        self.repo = PredictionRepository(db)
        self.user_repo = UserRepository(db)

    def predict_heart_disease(self, input_data: HeartDiseaseInput) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, str]]]:
        # Check if user exists
        user = self.user_repo.get_by_id(input_data.user_id)
        if not user:
            return None, {"error": "User not found"}
            
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
        
        model = HeartDiseaseModel()
        probability, prediction_result = model.predict(features)
        
        # Create prediction record in database
        prediction = Prediction(
            user_id=input_data.user_id,
            probability=probability,
            prediction=prediction_result
        )
        
        created_prediction = self.repo.create(prediction)
        
        return {
            "id": created_prediction.id,
            "user_id": created_prediction.user_id,
            "probability": created_prediction.probability,
            "prediction": created_prediction.prediction
        }, None
        
    def get_prediction(self, prediction_id: int) -> Optional[Prediction]:
        return self.repo.get_by_id(prediction_id)
        
    def get_user_predictions(self, user_id: int) -> List[Prediction]:
        return self.repo.get_by_user_id(user_id)
        
    def get_all_predictions(self) -> List[Prediction]:
        return self.repo.get_all()
        
    def delete_prediction(self, prediction_id: int) -> bool:
        prediction = self.repo.get_by_id(prediction_id)
        if prediction:
            self.repo.delete(prediction)
            return True
        return False