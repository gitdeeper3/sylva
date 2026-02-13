"""Rapid Spread Index (RSI) Calculator"""

import numpy as np
from typing import Dict


class RSICalculator:
    """
    Calculate Rapid Spread Index from nine normalized parameters.
    
    RSI = Σ(αᵢ × Pᵢ_norm)
    """
    
    def __init__(self, fuel_type: str = "pinus_halepensis"):
        self.fuel_type = fuel_type
        self.weights = self._get_weights()
    
    def _get_weights(self) -> Dict:
        """Get fuel type-specific weights."""
        weights = {
            "pinus_halepensis": {
                "lfm": 0.20, "dfm": 0.15, "cbd": 0.12, "sfl": 0.10,
                "fbd": 0.08, "wind": 0.15, "vpd": 0.08, "aspect": 0.06, "dc": 0.06
            },
            "quercus_ilex": {
                "lfm": 0.18, "dfm": 0.14, "cbd": 0.14, "sfl": 0.12,
                "fbd": 0.10, "wind": 0.14, "vpd": 0.07, "aspect": 0.05, "dc": 0.06
            },
            "mediterranean_maquis": {
                "lfm": 0.22, "dfm": 0.16, "cbd": 0.10, "sfl": 0.08,
                "fbd": 0.06, "wind": 0.16, "vpd": 0.09, "aspect": 0.07, "dc": 0.06
            },
            "dry_grassland": {
                "lfm": 0.15, "dfm": 0.18, "cbd": 0.08, "sfl": 0.12,
                "fbd": 0.10, "wind": 0.18, "vpd": 0.10, "aspect": 0.04, "dc": 0.05
            }
        }
        return weights.get(self.fuel_type, weights["pinus_halepensis"])
    
    def normalize_negative(self, value: float, p10: float, p100: float) -> float:
        """Normalize parameters with negative correlation."""
        if p100 <= p10:
            return 0.0
        norm = (p100 - value) / (p100 - p10)
        return np.clip(norm, 0.0, 1.0)
    
    def normalize_positive(self, value: float, p90: float, p0: float = 0.0) -> float:
        """Normalize parameters with positive correlation."""
        if p90 <= p0:
            return 0.0
        norm = (value - p0) / (p90 - p0)
        return np.clip(norm, 0.0, 1.0)
    
    def normalize_aspect(self, aspect: float) -> float:
        """Normalize terrain aspect."""
        aspect_rad = np.radians(aspect)
        target_rad = np.radians(225.0)
        norm = (1 + np.cos(aspect_rad - target_rad)) / 2
        return np.clip(norm, 0.0, 1.0)
    
    def normalize_parameters(self, parameters: Dict) -> Dict:
        """Normalize all parameters to 0-1 scale."""
        normalized = {}
        
        if "lfm" in parameters:
            normalized["lfm"] = self.normalize_negative(parameters["lfm"], 70.0, 200.0)
        if "dfm" in parameters:
            normalized["dfm"] = self.normalize_negative(parameters["dfm"], 6.0, 30.0)
        if "cbd" in parameters:
            normalized["cbd"] = self.normalize_positive(parameters["cbd"], 0.20)
        if "sfl" in parameters:
            normalized["sfl"] = self.normalize_positive(parameters["sfl"], 40.0)
        if "fbd" in parameters:
            normalized["fbd"] = self.normalize_positive(parameters["fbd"], 0.6)
        if "wind_speed" in parameters:
            normalized["wind"] = self.normalize_positive(parameters["wind_speed"], 10.0)
        if "vpd" in parameters:
            normalized["vpd"] = self.normalize_positive(parameters["vpd"], 30.0)
        if "aspect" in parameters:
            normalized["aspect"] = self.normalize_aspect(parameters["aspect"])
        if "drought_code" in parameters:
            normalized["dc"] = self.normalize_positive(parameters["drought_code"], 400.0)
        
        return normalized
    
    def calculate_rsi(self, normalized_params: Dict) -> float:
        """Calculate Rapid Spread Index (0-1)."""
        weighted_sum = 0.0
        total_weight = 0.0
        
        for param, value in normalized_params.items():
            if param in self.weights:
                weight = self.weights[param]
                weighted_sum += weight * value
                total_weight += weight
        
        if total_weight > 0:
            rsi = weighted_sum / total_weight
        else:
            rsi = 0.5
        
        return np.clip(rsi, 0.0, 1.0)
    
    def get_parameter_contributions(self, normalized_params: Dict) -> Dict:
        """Calculate individual parameter contributions."""
        contributions = {}
        rsi = self.calculate_rsi(normalized_params)
        
        for param, value in normalized_params.items():
            if param in self.weights and rsi > 0:
                weight = self.weights[param]
                contributions[param] = (weight * value) / rsi
        
        return contributions
