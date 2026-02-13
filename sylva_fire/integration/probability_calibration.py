"""Probability calibration for rapid spread forecasting"""

import numpy as np
from typing import Dict


class ProbabilityCalibrator:
    """
    Calibrate RSI to rapid spread probability.
    
    P(RS) = 1 / (1 + e^-(β₀ + β₁·RSI + β₂·RSI² + β₃·C))
    """
    
    def __init__(self, fuel_type: str = "pinus_halepensis"):
        self.fuel_type = fuel_type
        self.coefficients = self._load_coefficients()
    
    def _load_coefficients(self) -> Dict:
        """Load calibration coefficients."""
        coeffs = {
            "pinus_halepensis": {"beta_0": -4.8, "beta_1": 9.2, "beta_2": -4.1, "beta_3": 1.4},
            "quercus_ilex": {"beta_0": -4.5, "beta_1": 8.7, "beta_2": -3.8, "beta_3": 1.3},
            "mediterranean_maquis": {"beta_0": -4.3, "beta_1": 8.5, "beta_2": -3.6, "beta_3": 1.2},
            "dry_grassland": {"beta_0": -3.9, "beta_1": 7.8, "beta_2": -3.2, "beta_3": 1.1}
        }
        return coeffs.get(self.fuel_type, coeffs["pinus_halepensis"])
    
    def calibrate_probability(self, rsi: float, confidence: float = 1.0) -> float:
        """Convert RSI to calibrated probability."""
        beta_0 = self.coefficients["beta_0"]
        beta_1 = self.coefficients["beta_1"]
        beta_2 = self.coefficients["beta_2"]
        beta_3 = self.coefficients["beta_3"]
        
        logit = beta_0 + beta_1 * rsi + beta_2 * (rsi ** 2) + beta_3 * confidence
        probability = 1.0 / (1.0 + np.exp(-logit))
        
        return np.clip(probability, 0.0, 1.0)
