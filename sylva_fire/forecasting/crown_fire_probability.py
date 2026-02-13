"""Crown Fire Probability and Transition Model"""

import numpy as np
from typing import Dict

class CrownFireProbabilityModel:
    """
    Calculate probability of surface-to-crown fire transition.
    
    Based on Van Wagner (1977) with Mediterranean calibration.
    """
    
    def __init__(self):
        # Critical thresholds for Mediterranean species
        self.cbd_thresholds = {
            'pinus_halepensis': 0.10,
            'pinus_pinaster': 0.12,
            'quercus_ilex': 0.15,
            'mediterranean_maquis': 0.18
        }
        
        self.cbh_thresholds = {
            'pinus_halepensis': 4.0,
            'pinus_pinaster': 5.0,
            'quercus_ilex': 3.0,
            'mediterranean_maquis': 1.5
        }
    
    def calculate_crown_fire_probability(self,
                                        surface_intensity: float,
                                        canopy_bulk_density: float,
                                        canopy_base_height: float,
                                        foliar_moisture: float,
                                        wind_speed: float,
                                        fuel_type: str = 'pinus_halepensis') -> Dict:
        """
        Calculate probability of crown fire initiation and sustained spread.
        """
        
        # 1. Critical intensity for crown initiation (Van Wagner)
        I_c = (0.010 * canopy_base_height * (460 + 25.9 * foliar_moisture)) ** 1.5
        
        # 2. Intensity ratio
        intensity_ratio = surface_intensity / I_c if I_c > 0 else 0
        
        # 3. CBD adequacy
        cbd_threshold = self.cbd_thresholds.get(fuel_type, 0.10)
        cbd_ratio = canopy_bulk_density / cbd_threshold if cbd_threshold > 0 else 0
        
        # 4. Wind effect on crown fire spread
        wind_factor = 1 + (wind_speed / 20)
        
        # 5. Crown fire initiation probability (logistic)
        if intensity_ratio < 0.5:
            init_prob = 0.05
        elif intensity_ratio < 1.0:
            init_prob = 0.3 + 0.5 * (intensity_ratio - 0.5)
        elif intensity_ratio < 1.5:
            init_prob = 0.8 + 0.15 * (intensity_ratio - 1.0)
        else:
            init_prob = 0.95
        
        # 6. Crown fire spread probability
        if cbd_ratio < 0.8:
            spread_prob = init_prob * 0.3
        elif cbd_ratio < 1.2:
            spread_prob = init_prob * 0.7
        else:
            spread_prob = init_prob * 1.0
        
        spread_prob = min(0.95, spread_prob)
        
        # 7. Determine crown fire type
        if init_prob < 0.3:
            crown_fire_type = "Surface fire only"
            crown_color = "🟢"
        elif init_prob < 0.6:
            crown_fire_type = "Passive crown fire (torching)"
            crown_color = "🟡"
        elif init_prob < 0.8:
            crown_fire_type = "Active crown fire possible"
            crown_color = "🟠"
        else:
            crown_fire_type = "Active crown fire sustained"
            crown_color = "🔴"
        
        # 8. Spotting potential
        if spread_prob > 0.7 and wind_speed > 8:
            spotting = "VERY HIGH - Long distance spotting (>1.5 km)"
        elif spread_prob > 0.5 and wind_speed > 6:
            spotting = "HIGH - Moderate distance spotting (500-1500m)"
        elif spread_prob > 0.3:
            spotting = "MODERATE - Short distance spotting (<500m)"
        else:
            spotting = "LOW - Minimal spotting"
        
        return {
            "crown_fire_initiation_probability": round(init_prob, 3),
            "crown_fire_spread_probability": round(spread_prob, 3),
            "crown_fire_type": crown_fire_type,
            "crown_fire_color": crown_color,
            "critical_intensity_kW_m": round(I_c, 1),
            "intensity_ratio": round(intensity_ratio, 2),
            "cbd_ratio": round(cbd_ratio, 2),
            "spotting_potential": spotting,
            "wind_factor": round(wind_factor, 2),
            "torching_potential": "HIGH" if init_prob > 0.6 else "MODERATE" if init_prob > 0.3 else "LOW",
            "crown_fire_hazard": self._get_hazard_level(init_prob, spread_prob)
        }
    
    def _get_hazard_level(self, init_prob: float, spread_prob: float) -> str:
        """Get crown fire hazard level"""
        combined = (init_prob + spread_prob) / 2
        if combined < 0.2:
            return "LOW"
        elif combined < 0.4:
            return "MODERATE"
        elif combined < 0.6:
            return "HIGH"
        elif combined < 0.8:
            return "VERY HIGH"
        else:
            return "EXTREME"
    
    def estimate_crown_fire_ros(self, 
                               surface_ros: float,
                               crown_fire_prob: float,
                               wind_speed: float) -> float:
        """Estimate crown fire rate of spread"""
        if crown_fire_prob < 0.3:
            return surface_ros
        elif crown_fire_prob < 0.6:
            return surface_ros * 1.5
        elif crown_fire_prob < 0.8:
            return surface_ros * 2.5
        else:
            return surface_ros * 4.0
