"""Main rapid spread forecasting engine"""

import numpy as np
from typing import Dict, Optional
from datetime import datetime

from sylva_fire.integration.rsi_calculator import RSICalculator
from sylva_fire.integration.probability_calibration import ProbabilityCalibrator
from sylva_fire.integration.confidence_estimator import ConfidenceEstimator
from sylva_fire.core.rothermel import RothermelModel
from sylva_fire.core.byram import ByramIntensity
from sylva_fire.core.van_wagner import VanWagnerCrownFire


class RapidSpreadForecaster:
    """
    Main forecasting engine for rapid fire spread probability.
    
    Integrates nine parameters into unified rapid spread probability.
    """
    
    THRESHOLDS = {
        "normal": (0.0, 0.2),
        "elevated": (0.2, 0.4),
        "watch": (0.4, 0.6),
        "warning": (0.6, 0.8),
        "imminent": (0.8, 1.0)
    }
    
    def __init__(self, fuel_type: str = "pinus_halepensis"):
        self.fuel_type = fuel_type
        self.rsi_calculator = RSICalculator(fuel_type)
        self.calibrator = ProbabilityCalibrator(fuel_type)
        self.confidence_estimator = ConfidenceEstimator()
        self.rothermel = RothermelModel(fuel_type)
        self.byram = ByramIntensity()
        self.van_wagner = VanWagnerCrownFire(fuel_type)
    
    def predict(self,
               lfm: Optional[float] = None,
               dfm: Optional[float] = None,
               cbd: Optional[float] = None,
               sfl: Optional[float] = None,
               fbd: Optional[float] = None,
               wind_speed: Optional[float] = None,
               vpd: Optional[float] = None,
               aspect: Optional[float] = None,
               drought_code: Optional[float] = None,
               slope: float = 0.0,
               **kwargs) -> Dict:
        """Predict rapid spread probability."""
        
        # Collect parameters
        params = {
            "lfm": lfm,
            "dfm": dfm,
            "cbd": cbd,
            "sfl": sfl,
            "fbd": fbd,
            "wind_speed": wind_speed,
            "vpd": vpd,
            "aspect": aspect,
            "drought_code": drought_code
        }
        params = {k: v for k, v in params.items() if v is not None}
        
        # Calculate RSI
        normalized = self.rsi_calculator.normalize_parameters(params)
        rsi = self.rsi_calculator.calculate_rsi(normalized)
        
        # Calculate confidence
        confidence = self.confidence_estimator.estimate(params)
        
        # Calculate probability
        probability = self.calibrator.calibrate_probability(rsi, confidence)
        
        # Calculate ROS
        ros = self.rothermel.calculate_rate_of_spread(
            fuel_moisture=params.get("dfm", 15.0),
            wind_speed=params.get("wind_speed", 5.0),
            slope=slope
        )
        
        # Determine hazard level
        hazard_level = self._get_hazard_level(probability)
        
        # Estimate lead time
        lead_time = self._estimate_lead_time(probability)
        
        # Parameter contributions
        contributions = self.rsi_calculator.get_parameter_contributions(normalized)
        
        return {
            "probability": probability,
            "confidence": confidence,
            "lead_time": lead_time,
            "rsi": rsi,
            "hazard_level": hazard_level,
            "rate_of_spread": ros,
            "parameters": params,
            "normalized_parameters": normalized,
            "parameter_contributions": contributions,
            "timestamp": datetime.now().isoformat()
        }
    
    def _estimate_lead_time(self, probability: float) -> int:
        """Estimate early warning lead time in minutes."""
        if probability >= 0.8:
            return 60
        elif probability >= 0.6:
            return 90
        elif probability >= 0.4:
            return 120
        else:
            return 180
    
    def _get_hazard_level(self, probability: float) -> str:
        """Get hazard level from probability."""
        for level, (low, high) in self.THRESHOLDS.items():
            if low <= probability < high:
                return level
        return "normal"
    
    def get_decision_support(self, probability: float) -> Dict:
        """Get decision support recommendations."""
        level = self._get_hazard_level(probability)
        
        actions = {
            "normal": {
                "action": "Routine monitoring",
                "public_message": "Normal fire danger conditions"
            },
            "elevated": {
                "action": "Enhanced situational awareness",
                "public_message": "Conditions favor fire growth"
            },
            "watch": {
                "action": "Pre-positioning, public information",
                "public_message": "Very dry fuels and increasing winds"
            },
            "warning": {
                "action": "Resource mobilization, evacuation preparation",
                "public_message": "Conditions favorable for rapid fire spread"
            },
            "imminent": {
                "action": "Evacuation execution, full response activation",
                "public_message": "Rapid fire spread expected - evacuate now"
            }
        }
        
        return actions.get(level, actions["normal"])
