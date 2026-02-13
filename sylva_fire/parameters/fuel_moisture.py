"""Fuel moisture calculations - Live Fuel Moisture (LFM) and Dead Fuel Moisture (DFM)"""

import numpy as np
from typing import Dict


class FuelMoistureCalculator:
    """Calculate live and dead fuel moisture content."""
    
    def __init__(self):
        self.LFM_CRITICAL = {
            "pinus_halepensis": 85.0,
            "quercus_ilex": 75.0,
            "mediterranean_maquis": 80.0,
            "dry_grassland": 70.0
        }
    
    def estimate_lfm_from_ndwi(self, ndwi: float) -> float:
        """Estimate Live Fuel Moisture from NDWI."""
        lfm = 50.0 + (ndwi * 100.0)
        return np.clip(lfm, 30, 200)
    
    def classify_lfm_hazard(self, lfm: float, species: str = "pinus_halepensis") -> Dict:
        """Classify LFM hazard level."""
        critical = self.LFM_CRITICAL.get(species, 85.0)
        
        if lfm >= 120:
            level = "Very High"
        elif lfm >= 100:
            level = "High"
        elif lfm >= 80:
            level = "Moderate"
        elif lfm >= 60:
            level = "Low"
        else:
            level = "Very Low"
        
        return {
            "lfm_percent": lfm,
            "hazard_level": level,
            "below_critical": lfm < critical
        }
    
    def calculate_vpd(self, temperature: float, humidity: float) -> float:
        """Calculate Vapor Pressure Deficit (hPa)."""
        e_s = 6.1078 * np.exp((17.27 * temperature) / (temperature + 237.3))
        e = e_s * (humidity / 100.0)
        return e_s - e
