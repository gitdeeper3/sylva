"""Confidence estimation for rapid spread forecasts"""

import numpy as np
from typing import Dict


class ConfidenceEstimator:
    """Estimate forecast confidence based on data quality."""
    
    def __init__(self):
        self.weights = {
            "data_completeness": 0.50,
            "data_quality": 0.30,
            "model_uncertainty": 0.20
        }
    
    def estimate(self, parameters: Dict) -> float:
        """Estimate overall forecast confidence (0-1)."""
        # Required parameters
        required = ["lfm", "dfm", "wind_speed"]
        if "cbd" in parameters:
            required.append("cbd")
            
        # Completeness score (0-1)
        present = sum(1 for p in required if p in parameters and parameters[p] is not None)
        completeness = present / len(required)
        
        # Quality score - based on parameter ranges
        quality = 0.8
        penalties = 0
        
        if "lfm" in parameters:
            if parameters["lfm"] < 30 or parameters["lfm"] > 200:
                penalties += 0.2
        if "dfm" in parameters:
            if parameters["dfm"] < 1 or parameters["dfm"] > 30:
                penalties += 0.2
        if "wind_speed" in parameters:
            if parameters["wind_speed"] < 0 or parameters["wind_speed"] > 40:
                penalties += 0.2
                
        quality = max(0.4, 0.8 - penalties)
        
        # Model uncertainty
        model_uncertainty = 0.7  # Default
        
        # Calculate confidence
        confidence = (0.5 * completeness + 
                     0.3 * quality + 
                     0.2 * model_uncertainty)
        
        # Scale to realistic range (0.4-0.8 for most cases)
        confidence = 0.4 + (confidence * 0.4)
        
        return np.clip(confidence, 0.2, 0.9)
    
    def categorize_confidence(self, confidence: float) -> str:
        """Categorize confidence level."""
        if confidence >= 0.75:
            return "Very High"
        elif confidence >= 0.65:
            return "High"
        elif confidence >= 0.50:
            return "Moderate"
        elif confidence >= 0.35:
            return "Low"
        else:
            return "Very Low"
