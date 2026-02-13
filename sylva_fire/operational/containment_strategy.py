"""Containment Difficulty and Resource Optimization - Strategic Decision Support"""

import numpy as np
from typing import Dict, List, Tuple, Optional

class ContainmentStrategyEngine:
    """
    Advanced containment difficulty assessment with resource optimization.
    
    Factors:
    - ROS & Flame Length
    - Terrain complexity
    - Fuel type
    - Wind speed
    - Access difficulty
    - WUI proximity
    """
    
    def __init__(self):
        # Baseline difficulty weights
        self.weights = {
            'ros': 0.30,
            'flame': 0.25,
            'terrain': 0.20,
            'fuel': 0.15,
            'access': 0.10
        }
        
        # Fuel type difficulty factors
        self.fuel_difficulty = {
            'dry_grassland': 0.6,
            'pinus_halepensis': 1.2,
            'quercus_ilex': 1.3,
            'mediterranean_maquis': 1.8,
            'pinus_pinaster': 1.4,
            'eucalyptus': 1.6
        }
    
    def assess_containment(self,
                          ros: float,
                          flame_length: float,
                          fuel_type: str,
                          wind_speed: float,
                          slope: float,
                          wui_proximity_km: float = 5.0,
                          access_difficulty: float = 0.5) -> Dict:
        """
        Comprehensive containment difficulty assessment.
        """
        
        # 1. Rate of spread contribution
        ros_score = min(1.0, ros / 50) * self.weights['ros']
        
        # 2. Flame length contribution
        if flame_length < 1.2:
            flame_score = 0.1 * self.weights['flame']
        elif flame_length < 2.4:
            flame_score = 0.4 * self.weights['flame']
        elif flame_length < 3.4:
            flame_score = 0.7 * self.weights['flame']
        elif flame_length < 10:
            flame_score = 0.9 * self.weights['flame']
        else:
            flame_score = 1.0 * self.weights['flame']
        
        # 3. Terrain contribution
        terrain_score = min(1.0, slope / 30) * self.weights['terrain']
        
        # 4. Fuel type contribution
        fuel_mult = self.fuel_difficulty.get(fuel_type, 1.0)
        fuel_score = fuel_mult * 0.6 * self.weights['fuel']
        
        # 5. Access difficulty
        access_score = access_difficulty * self.weights['access']
        
        # 6. Wind penalty
        wind_penalty = min(0.3, wind_speed / 40)
        
        # Calculate total difficulty score
        base_score = ros_score + flame_score + terrain_score + fuel_score + access_score
        total_score = min(1.0, base_score * (1 + wind_penalty))
        
        # Determine containment class
        if total_score < 0.25:
            containment_class = "LOW"
            color = "🟢"
            initial_attack = "HIGHLY FEASIBLE"
            time_to_contain_hr = 0.5
            success_probability = 0.9
        elif total_score < 0.45:
            containment_class = "MODERATE"
            color = "🟡"
            initial_attack = "FEASIBLE WITH RESOURCES"
            time_to_contain_hr = 1.5
            success_probability = 0.7
        elif total_score < 0.65:
            containment_class = "DIFFICULT"
            color = "🟠"
            initial_attack = "LIMITED - EXTENDED ATTACK"
            time_to_contain_hr = 3.0
            success_probability = 0.5
        elif total_score < 0.85:
            containment_class = "VERY DIFFICULT"
            color = "🔴"
            initial_attack = "NOT FEASIBLE"
            time_to_contain_hr = 6.0
            success_probability = 0.3
        else:
            containment_class = "EXTREME"
            color = "⚫"
            initial_attack = "IMPOSSIBLE - DEFENSIVE ONLY"
            time_to_contain_hr = 12.0
            success_probability = 0.1
        
        # Calculate resource requirements
        resources = self._calculate_resources(
            total_score, 
            time_to_contain_hr,
            wui_proximity_km
        )
        
        # WUI threat assessment
        wui_threat = self._assess_wui_threat(total_score, wui_proximity_km, ros)
        
        return {
            "containment_difficulty": {
                "score": round(total_score, 2),
                "class": containment_class,
                "color": color
            },
            "initial_attack_feasibility": initial_attack,
            "estimated_containment_time_hr": time_to_contain_hr,
            "containment_success_probability": round(success_probability, 2),
            "critical_factors": self._get_critical_factors(
                ros_score, flame_score, terrain_score, fuel_score
            ),
            "resource_recommendations": resources,
            "wui_assessment": wui_threat,
            "strategic_priority": self._get_strategic_priority(total_score, wui_proximity_km)
        }
    
    def _calculate_resources(self, difficulty: float, time_to_contain: float, wui_distance: float) -> Dict:
        """Calculate optimal resource requirements"""
        
        base_crews = max(2, int(difficulty * 20))
        base_engines = max(1, int(difficulty * 15))
        
        # WUI adjustment
        wui_multiplier = 2.0 if wui_distance < 1.0 else 1.5 if wui_distance < 3.0 else 1.0
        
        return {
            "hand_crews": int(base_crews * wui_multiplier),
            "fire_engines": int(base_engines * wui_multiplier * 0.7),
            "air_tankers": max(1, int(difficulty * 5)),
            "helicopters": max(1, int(difficulty * 4)),
            "dozers": max(1, int(difficulty * 3)),
            "overhead": "Type 1" if difficulty > 0.6 else "Type 2" if difficulty > 0.3 else "Type 3",
            "estimated_cost_usd": int(base_crews * time_to_contain * 5000 * wui_multiplier)
        }
    
    def _assess_wui_threat(self, difficulty: float, distance_km: float, ros: float) -> Dict:
        """Assess threat to Wildland-Urban Interface"""
        
        time_to_wui = (distance_km * 1000) / (ros * 60) if ros > 0 else float('inf')
        
        if distance_km < 1.0:
            threat_level = "CRITICAL"
            color = "⚫"
            evacuation = "IMMEDIATE"
        elif distance_km < 3.0:
            threat_level = "HIGH"
            color = "🔴"
            evacuation = "PREPARE"
        elif distance_km < 5.0:
            threat_level = "MODERATE"
            color = "🟠"
            evacuation = "WATCH"
        else:
            threat_level = "LOW"
            color = "🟡"
            evacuation = "MONITOR"
        
        return {
            "threat_level": threat_level,
            "color": color,
            "distance_km": distance_km,
            "estimated_arrival_min": round(time_to_wui, 0) if time_to_wui != float('inf') else "N/A",
            "evacuation_status": evacuation,
            "structure_threat_count": self._estimate_structures_at_risk(distance_km)
        }
    
    def _get_critical_factors(self, ros: float, flame: float, terrain: float, fuel: float) -> List[str]:
        """Identify the most critical containment factors"""
        factors = []
        
        if ros > 0.25:
            factors.append("High rate of spread")
        if flame > 0.2:
            factors.append("Extreme flame length")
        if terrain > 0.15:
            factors.append("Complex terrain")
        if fuel > 0.1:
            factors.append("Challenging fuel type")
            
        return factors[:3]  # Return top 3
    
    def _get_strategic_priority(self, difficulty: float, wui_distance: float) -> str:
        """Determine strategic priority level"""
        if difficulty > 0.7 or wui_distance < 1.0:
            return "CRITICAL - National Resource Consideration"
        elif difficulty > 0.5 or wui_distance < 3.0:
            return "HIGH - Regional Resource Mobilization"
        elif difficulty > 0.3:
            return "MODERATE - Local Resource Allocation"
        else:
            return "ROUTINE - Standard Dispatch"
    
    def _estimate_structures_at_risk(self, distance_km: float) -> str:
        """Estimate number of structures at risk"""
        if distance_km < 1.0:
            return "500+"
        elif distance_km < 3.0:
            return "100-500"
        elif distance_km < 5.0:
            return "20-100"
        else:
            return "<20"
