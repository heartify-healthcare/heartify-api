from pydantic import BaseModel, Field, validator
from typing import Optional

class HeartDiseaseInput(BaseModel):
    user_id: int = Field(..., description="ID of the user making the prediction")
    age: int = Field(..., ge=0, le=120, description="Age in years")
    sex: int = Field(..., ge=0, le=1, description="Sex (0 = female, 1 = male)")
    cp: int = Field(..., ge=0, le=4, description="Chest pain type (0-4)")
    trestbps: int = Field(..., ge=0, description="Resting blood pressure (in mm Hg)")
    chol: int = Field(..., ge=0, description="Serum cholesterol in mg/dl")
    fbs: int = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)")
    restecg: int = Field(..., ge=0, le=2, description="Resting electrocardiographic results (0, 1, 2)")
    thalach: int = Field(..., ge=0, description="Maximum heart rate achieved")
    exang: int = Field(..., ge=0, le=1, description="Exercise induced angina (1 = yes, 0 = no)")
    oldpeak: float = Field(..., ge=0.0, description="ST depression induced by exercise relative to rest")
    slope: int = Field(..., ge=0, le=3, description="The slope of the peak exercise ST segment")
    
    @validator('age')
    def age_must_be_reasonable(cls, v):
        if v < 18 or v > 100:
            raise ValueError("Age should be between 18 and 100")
        return v
    
    @validator('trestbps')
    def trestbps_must_be_reasonable(cls, v):
        if v < 50 or v > 300:
            raise ValueError("Resting blood pressure should be between 50 and 300")
        return v
    
    @validator('chol')
    def chol_must_be_reasonable(cls, v):
        if v < 50 or v > 700:
            raise ValueError("Cholesterol should be between 50 and 700")
        return v
    
    @validator('thalach')
    def thalach_must_be_reasonable(cls, v):
        if v < 50 or v > 300:
            raise ValueError("Maximum heart rate should be between 50 and 300")
        return v


class PredictionResponse(BaseModel):
    id: int
    user_id: int
    probability: float = Field(..., ge=0.0, le=1.0, description="Probability of having heart disease")
    prediction: str = Field(..., description="Prediction result (POSITIVE or NEGATIVE)")
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 2,
                "probability": 0.75,
                "prediction": "POSITIVE"
            }
        }