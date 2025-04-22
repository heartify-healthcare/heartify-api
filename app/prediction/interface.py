from abc import ABC, abstractmethod
from typing import Dict, Any, List
import numpy as np

class PredictionInterface(ABC):
    """Interface for heart disease prediction services."""
    
    @abstractmethod
    def predict(self, features: List[float]) -> Dict[str, Any]:
        """
        Make a heart disease prediction based on input features.
        
        Args:
            features: List of features in the correct order for prediction
            
        Returns:
            Dictionary containing prediction probability and result
        """
        pass