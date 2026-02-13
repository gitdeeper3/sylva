"""Fire Spread Distance and Impact Radius Estimation"""

import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta

class SpreadDistanceProjector:
    """
    Estimate potential fire spread distance and impact areas.
    """
    
    def __init__(self):
        # Wind alignment factors
        self.alignment_factors = {
            'perfect': 1.0,
            'high': 0.8,
            'partial': 0.6,
            'low': 0.4,
            'opposing': 0.2
        }
    
    def calculate_potential_spread(self,
                                  ros: float,
                                  wind_speed: float,
                                  wind_direction: int,
                                  slope: float,
                                  slope_aspect: int,
                                  lead_time: int = 90,
                                  fuel_continuity: float = 0.8) -> Dict:
        """
        Calculate potential spread distance and impact radius.
        """
        
        # 1. Base spread distance
        base_distance = (ros / 60) * lead_time  # km
        
        # 2. Wind-slope alignment score
        alignment_score = self._calculate_alignment(wind_direction, slope_aspect)
        
        # 3. Terrain adjustment
        terrain_factor = 1 + (slope / 100) * 0.5
        
        # 4. Fuel continuity adjustment
        continuity_factor = 0.5 + (fuel_continuity * 0.5)
        
        # 5. Adjusted spread distance
        adjusted_distance = base_distance * alignment_score * terrain_factor * continuity_factor
        
        # 6. Head fire distance
        head_distance = adjusted_distance
        
        # 7. Flank fire distance
        flank_distance = head_distance * 0.4
        
        # 8. Backing fire distance
        backing_distance = head_distance * 0.1
        
        # 9. Impact radius (WUI risk)
        impact_radius = head_distance * 0.8
        
        # 10. Arrival time estimates
        arrival_times = self._calculate_arrival_times(head_distance)
        
        return {
            "head_fire_distance_km": round(head_distance, 1),
            "flank_fire_distance_km": round(flank_distance, 1),
            "backing_fire_distance_km": round(backing_distance, 1),
            "impact_radius_km": round(impact_radius, 1),
            "potential_burned_area_ha": round(self._estimate_burned_area(head_distance), 1),
            "alignment_score": round(alignment_score, 2),
            "alignment_category": self._get_alignment_category(alignment_score),
            "arrival_times": arrival_times,
            "evacuation_zone_km": round(head_distance * 1.5, 1),
            "warning_zone_km": round(head_distance * 2.5, 1),
            "components": {
                "base_distance_km": round(base_distance, 1),
                "terrain_factor": round(terrain_factor, 2),
                "continuity_factor": round(continuity_factor, 2)
            }
        }
    
    def _calculate_alignment(self, wind_dir: int, slope_aspect: int) -> float:
        """Calculate wind-slope alignment score (0-1)"""
        diff = abs(wind_dir - slope_aspect)
        diff = min(diff, 360 - diff)
        
        if diff < 30:
            return 1.0
        elif diff < 60:
            return 0.8
        elif diff < 90:
            return 0.6
        elif diff < 135:
            return 0.4
        else:
            return 0.2
    
    def _get_alignment_category(self, score: float) -> str:
        """Categorize alignment score"""
        if score >= 0.8:
            return "PERFECT - Maximum spread potential"
        elif score >= 0.6:
            return "HIGH - Favorable alignment"
        elif score >= 0.4:
            return "PARTIAL - Moderate alignment"
        elif score >= 0.2:
            return "LOW - Poor alignment"
        else:
            return "OPPOSING - Spread limited"
    
    def _estimate_burned_area(self, head_distance: float) -> float:
        """Estimate potential burned area (hectares)"""
        # Simplified elliptical fire growth model
        length = head_distance * 1000  # convert to meters
        width = length * 0.6
        area_m2 = (length * width * 3.14159) / 4  # ellipse area
        return area_m2 / 10000  # convert to hectares
    
    def _calculate_arrival_times(self, head_distance: float) -> List[Dict]:
        """Calculate arrival times at key distances"""
        arrival_times = []
        distances = [1, 2, 5, 10]  # km
        
        for dist in distances:
            if head_distance > 0:
                minutes = (dist / head_distance) * 90
                arrival_time = datetime.now() + timedelta(minutes=minutes)
                arrival_times.append({
                    "distance_km": dist,
                    "estimated_arrival": arrival_time.strftime("%H:%M"),
                    "minutes_from_now": round(minutes, 0)
                })
        
        return arrival_times
    
    def get_threatened_assets(self, 
                             head_distance: float,
                             wui_present: bool = True,
                             critical_infrastructure: bool = False) -> Dict:
        """Estimate threatened assets"""
        
        threat_level = "LOW"
        if head_distance > 10:
            threat_level = "EXTREME"
        elif head_distance > 5:
            threat_level = "HIGH"
        elif head_distance > 2:
            threat_level = "MODERATE"
        
        return {
            "threat_level": threat_level,
            "evacuation_priority": "IMMEDIATE" if head_distance > 5 else "STAND BY",
            "wui_risk": "HIGH" if wui_present and head_distance > 3 else "MODERATE",
            "infrastructure_risk": "CRITICAL" if critical_infrastructure and head_distance > 4 else "NORMAL"
        }
