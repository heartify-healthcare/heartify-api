from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any

class HeartDiseaseInputSchema(BaseModel):
    """Schema for heart disease prediction input data.
    
    The order and names must match the training data columns.
    """
    age: float = Field(..., description="Age in years")
    sex: int = Field(..., description="Sex (1 = male, 0 = female)")
    cp: int = Field(..., description="Chest pain type (0-4)")
    trestbps: float = Field(..., description="Resting blood pressure (in mm Hg)")
    chol: float = Field(..., description="Serum cholesterol in mg/dl")
    fbs: int = Field(..., description="Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)")
    restecg: int = Field(..., description="Resting electrocardiographic results (0-2)")
    thalach: float = Field(..., description="Maximum heart rate achieved")
    exang: int = Field(..., description="Exercise induced angina (1 = yes; 0 = no)")
    oldpeak: float = Field(..., description="ST depression induced by exercise relative to rest")
    slope: int = Field(..., description="Slope of the peak exercise ST segment (0-2)")
    
    @validator('sex', 'cp', 'fbs', 'restecg', 'exang', 'slope')
    def validate_categorical(cls, v, values, field):
        """Validate that categorical variables are in their proper ranges."""
        ranges = {
            'sex': [0, 1],
            'cp': [0, 1, 2, 3, 4],
            'fbs': [0, 1],
            'restecg': [0, 1, 2],
            'exang': [0, 1],
            'slope': [0, 1, 2],
        }
        if v not in ranges[field.name]:
            raise ValueError(f"{field.name} must be one of {ranges[field.name]}")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": 52,
                "sex": 1,
                "cp": 4,
                "trestbps": 160,
                "chol": 246,
                "fbs": 0,
                "restecg": 1,
                "thalach": 82,
                "exang": 1,
                "oldpeak": 4.0,
                "slope": 2
            }
        }

class PredictionResponseSchema(BaseModel):
    """Schema for heart disease prediction response."""
    probability: float = Field(..., description="Probability of heart disease")
    prediction: str = Field(..., description="Prediction result (POSITIVE or NEGATIVE)")
    
    class Config:
        schema_extra = {
            "example": {
                "probability": 0.87,
                "prediction": "POSITIVE"
            }
        }

class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")