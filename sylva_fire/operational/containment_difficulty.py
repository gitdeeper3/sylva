"""Containment Difficulty Index for operational decision support"""

import numpy as np
from typing import Dict, Tuple

class ContainmentDifficultyIndex:
    """
    Calculate suppression difficulty based on fire behavior and terrain.
    
    Factors:
    - Rate of Spread (ROS)
    - Flame Length (FL)
    - Fuel Type
    - Slope
    - Wind Speed
    - Fuel Continuity
    """
    
    def __init__(self):
        # Difficulty thresholds
        self.thresholds = {
            'ros': {'low': 10, 'moderate': 20, 'difficult': 35, 'very_difficult': 50},
            'flame': {'low': 1.2, 'moderate': 2.4, 'difficult': 3.4, 'very_difficult': 10},
            'slope': {'low': 10, 'moderate': 20, 'difficult': 35, 'very_difficult': 50}
        }
        
        # Fuel type difficulty multipliers
        self.fuel_multiplier = {
            'dry_grassland': 0.8,
            'pinus_halepensis': 1.2,
            'quercus_ilex': 1.3,
            'mediterranean_maquis': 1.5,
            'pinus_pinaster': 1.4
        }
    
    def calculate_cdi(self, 
                     ros: float,
                     flame_length: float,
                     fuel_type: str,
                     slope: float = 0,
                     wind_speed: float = 0,
                     fuel_continuity: float = 0.8) -> Dict:
        """
        Calculate Containment Difficulty Index (0-100).
        
        Returns:
            CDI score and suppression recommendations
        """
        
        # 1. ROS contribution (0-40)
        ros_score = min(40, (ros / 60) * 40)
        
        # 2. Flame length contribution (0-30)
        flame_score = min(30, (flame_length / 15) * 30)
        
        # 3. Slope contribution (0-15)
        slope_score = min(15, (slope / 45) * 15)
        
        # 4. Fuel type multiplier
        fuel_mult = self.fuel_multiplier.get(fuel_type, 1.0)
        
        # 5. Wind contribution (0-10)
        wind_score = min(10, (wind_speed / 20) * 10)
        
        # 6. Fuel continuity (0-5)
        continuity_score = fuel_continuity * 5
        
        # Calculate CDI
        cdi = (ros_score + flame_score + slope_score + wind_score + continuity_score) * fuel_mult
        cdi = min(100, max(0, cdi))
        
        # Determine difficulty level
        if cdi < 20:
            level = "LOW"
            color = "🟢"
            handline = "Handline construction possible"
            dozer = "Dozer line effective"
            aerial = "Standard air tanker"
            tactic = "Direct attack"
        elif cdi < 40:
            level = "MODERATE"
            color = "🟡"
            handline = "Handline difficult, mechanical assist needed"
            dozer = "Dozer line possible with multiple passes"
            aerial = "Heavy air tankers recommended"
            tactic = "Parallel attack"
        elif cdi < 60:
            level = "DIFFICULT"
            color = "🟠"
            handline = "Handline not feasible"
            dozer = "Dozer line very difficult"
            aerial = "Multiple heavy air tankers"
            tactic = "Indirect attack"
        elif cdi < 80:
            level = "VERY DIFFICULT"
            color = "🔴"
            handline = "Impossible"
            dozer = "Dozer line ineffective"
            aerial = "Aerial only, limited effectiveness"
            tactic = "Indirect attack, structure protection"
        else:
            level = "EXTREME"
            color = "⚫"
            handline = "No suppression effective"
            dozer = "No dozer line possible"
            aerial = "Aerial ineffective, safety hazard"
            tactic = "Evacuation only, defensive"
        
        return {
            "cdi_score": round(cdi, 1),
            "cdi_level": level,
            "cdi_color": color,
            "handline_feasibility": handline,
            "dozer_feasibility": dozer,
            "aerial_effectiveness": aerial,
            "recommended_tactic": tactic,
            "direct_attack_possible": cdi < 40,
            "indirect_attack_needed": cdi >= 40,
            "evacuation_priority": "IMMEDIATE" if cdi >= 60 else "STAND BY",
            "components": {
                "ros_score": round(ros_score, 1),
                "flame_score": round(flame_score, 1),
                "slope_score": round(slope_score, 1),
                "wind_score": round(wind_score, 1),
                "continuity_score": round(continuity_score, 1),
                "fuel_multiplier": fuel_mult
            }
        }
    
    def get_suppression_resources(self, cdi_score: float, fire_size_ha: float) -> Dict:
        """Estimate required suppression resources"""
        
        base_crews = max(1, fire_size_ha / 10)
        
        if cdi_score < 20:
            crews = int(base_crews)
            engines = int(crews * 0.5)
            air_tankers = 1
            helicopters = 1
        elif cdi_score < 40:
            crews = int(base_crews * 1.5)
            engines = int(crews * 0.7)
            air_tankers = 2
            helicopters = 2
        elif cdi_score < 60:
            crews = int(base_crews * 2.5)
            engines = int(crews * 1)
            air_tankers = 3
            helicopters = 3
        elif cdi_score < 80:
            crews = int(base_crews * 4)
            engines = int(crews * 1.2)
            air_tankers = 4
            helicopters = 4
        else:
            crews = int(base_crews * 6)
            engines = int(crews * 1.5)
            air_tankers = 5
            helicopters = 5
        
        return {
            "hand_crews": crews,
            "fire_engines": engines,
            "air_tankers": air_tankers,
            "helicopters": helicopters,
            "dozers": max(1, int(fire_size_ha / 50))
        }
