"""Atmospheric parameters - Wind, VPD"""

import numpy as np
from typing import Dict


class AtmosphericCalculator:
    """Calculate atmospheric parameters."""
    
    def calculate_wind_adjustment_factor(self, canopy_cover: float) -> float:
        """Calculate canopy wind reduction factor."""
        if canopy_cover < 0.2:
            return 0.6
        elif canopy_cover < 0.5:
            return 0.4
        elif canopy_cover < 0.8:
            return 0.25
        else:
            return 0.15
    
    def classify_vpd_hazard(self, vpd: float) -> Dict:
        """Classify VPD hazard level."""
        if vpd < 5:
            level = "Very Low"
        elif vpd < 10:
            level = "Low"
        elif vpd < 15:
            level = "Moderate"
        elif vpd < 25:
            level = "High"
        elif vpd < 35:
            level = "Very High"
        else:
            level = "Extreme"
        
        return {
            "vpd_hPa": vpd,
            "hazard_level": level
        }
