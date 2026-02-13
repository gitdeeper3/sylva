"""Drought Code calculations"""

import numpy as np
from typing import Dict


class DroughtCodeCalculator:
    """Calculate Canadian Drought Code."""
    
    def calculate_drought_code(self,
                              dc_previous: float,
                              max_temp: float,
                              precipitation: float) -> float:
        """Calculate Drought Code."""
        if precipitation <= 2.8:
            P_eff = precipitation
        else:
            P_eff = 2.8 + 0.83 * (precipitation - 2.8)
        
        dc = dc_previous + 0.5 * (max_temp + 4.0) - P_eff
        return max(15.0, dc)
    
    def classify_dc_hazard(self, dc: float) -> Dict:
        """Classify Drought Code hazard level."""
        if dc < 100:
            level = "Very Low"
        elif dc < 200:
            level = "Low"
        elif dc < 300:
            level = "Moderate"
        elif dc < 400:
            level = "High"
        elif dc < 500:
            level = "Very High"
        else:
            level = "Extreme"
        
        return {
            "drought_code": dc,
            "hazard_level": level
        }
