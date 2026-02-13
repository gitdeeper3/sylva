"""Escalation Trend and Spread Distance Projection - Tactical Decision Support"""

import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta

class EscalationTrendAnalyzer:
    """
    Analyze fire environment trends and project spread distances.
    
    Key Indicators:
    - Wind trend (ΔVw)
    - VPD trend (ΔVPD)
    - DFM trend (ΔDFM)
    - Spread distance projection
    """
    
    def __init__(self):
        self.trend_thresholds = {
            'wind': {'rising': 2.0, 'falling': -2.0},
            'vpd': {'rising': 5.0, 'falling': -5.0},
            'dfm': {'drying': -1.0, 'wetting': 1.0}
        }
    
    def analyze_trends(self,
                      current_params: Dict,
                      historical_hourly: List[Dict]) -> Dict:
        """Analyze 3-hour trends in critical parameters."""
        
        if len(historical_hourly) < 3:
            return self._default_trend()
        
        # Get values from 3 hours ago
        past = historical_hourly[0]
        current = current_params
        
        # Calculate deltas
        wind_delta = current.get('wind_speed', 0) - past.get('wind_speed', 0)
        vpd_delta = current.get('vpd', 0) - past.get('vpd', 0)
        dfm_delta = past.get('dfm', 15) - current.get('dfm', 15)
        
        # Determine trends
        wind_trend = self._get_wind_trend(wind_delta)
        vpd_trend = self._get_vpd_trend(vpd_delta)
        dfm_trend = self._get_dfm_trend(dfm_delta)
        
        # Overall escalation score
        escalation_score = self._calculate_escalation_score(
            wind_delta, vpd_delta, dfm_delta
        )
        
        # Determine overall trend
        if escalation_score >= 0.6:
            overall = "🔴 ESCALATING RAPIDLY"
            decision_impact = "IMMEDIATE PRE-DEPLOYMENT REQUIRED"
            lead_time_reduction = -30
            trend_multiplier = 1.3
        elif escalation_score >= 0.3:
            overall = "🟠 ESCALATING"
            decision_impact = "PREPARE FOR PRE-DEPLOYMENT"
            lead_time_reduction = -15
            trend_multiplier = 1.15
        elif escalation_score >= -0.2:
            overall = "🟡 STABLE"
            decision_impact = "MAINTAIN CURRENT POSTURE"
            lead_time_reduction = 0
            trend_multiplier = 1.0
        else:
            overall = "🟢 MODERATING"
            decision_impact = "CONSIDER DOWNSIZING"
            lead_time_reduction = 15
            trend_multiplier = 0.85
        
        return {
            "overall_trend": overall,
            "escalation_score": round(escalation_score, 2),
            "decision_impact": decision_impact,
            "lead_time_adjustment": lead_time_reduction,
            "trend_multiplier": trend_multiplier,
            "wind": {
                "delta": round(wind_delta, 1),
                "trend": wind_trend,
                "icon": "↑" if wind_delta > 0 else "↓" if wind_delta < 0 else "→"
            },
            "vpd": {
                "delta": round(vpd_delta, 1),
                "trend": vpd_trend,
                "icon": "↑" if vpd_delta > 0 else "↓" if vpd_delta < 0 else "→"
            },
            "dfm": {
                "delta": round(dfm_delta, 1),
                "trend": dfm_trend,
                "icon": "↓" if dfm_delta > 0 else "↑" if dfm_delta < 0 else "→"
            }
        }
    
    def project_spread_distance(self,
                               ros: float,
                               lead_time: int = 90,
                               wind_trend: str = "🟡 STABLE",
                               terrain_factor: float = 1.0) -> Dict:
        """
        Project forward spread distance based on ROS and trends.
        """
        # CORRECTED: Convert ROS from m/min to km/min
        ros_km_per_min = ros / 1000  # Convert m/min to km/min
        
        # Base distance in km
        base_km = ros_km_per_min * lead_time
        
        # Get trend multiplier
        trend_multiplier = 1.0
        if "ESCALATING RAPIDLY" in wind_trend:
            trend_multiplier = 1.3
        elif "ESCALATING" in wind_trend:
            trend_multiplier = 1.15
        elif "MODERATING" in wind_trend:
            trend_multiplier = 0.85
        
        # Apply terrain factor (0.8-1.5)
        terrain_factor = min(1.5, max(0.8, terrain_factor))
        
        # Calculate projected distance
        projected_km = base_km * trend_multiplier * terrain_factor
        
        # Calculate threat zones
        return {
            "projected_distance_km": round(projected_km, 1),
            "distance_range_km": {
                "min": round(projected_km * 0.8, 1),
                "max": round(projected_km * 1.2, 1)
            },
            "threat_zone_ha": round(self._calculate_threat_area(projected_km), 1),
            "evacuation_buffer_km": round(projected_km * 1.5, 1),
            "arrival_times": self._calculate_arrival_times(projected_km, lead_time),
            "impact_assessment": self._assess_impact(projected_km)
        }
    
    def _get_wind_trend(self, delta: float) -> str:
        if delta >= self.trend_thresholds['wind']['rising']:
            return "INCREASING RAPIDLY"
        elif delta > 0:
            return "INCREASING"
        elif delta <= self.trend_thresholds['wind']['falling']:
            return "DECREASING RAPIDLY"
        elif delta < 0:
            return "DECREASING"
        else:
            return "STABLE"
    
    def _get_vpd_trend(self, delta: float) -> str:
        if delta >= self.trend_thresholds['vpd']['rising']:
            return "DRYING RAPIDLY"
        elif delta > 0:
            return "DRYING"
        elif delta <= self.trend_thresholds['vpd']['falling']:
            return "MOISTENING RAPIDLY"
        elif delta < 0:
            return "MOISTENING"
        else:
            return "STABLE"
    
    def _get_dfm_trend(self, delta: float) -> str:
        if delta >= 1.0:
            return "DRYING RAPIDLY"
        elif delta > 0:
            return "DRYING"
        elif delta <= -1.0:
            return "WETTING RAPIDLY"
        elif delta < 0:
            return "WETTING"
        else:
            return "STABLE"
    
    def _calculate_escalation_score(self, wind_delta: float, vpd_delta: float, dfm_delta: float) -> float:
        """Calculate overall escalation score (0-1)"""
        # Normalize deltas to 0-1 scale
        wind_score = self._normalize_delta(wind_delta, 5.0)
        vpd_score = self._normalize_delta(vpd_delta, 10.0)
        dfm_score = self._normalize_delta(dfm_delta, 2.0)
        
        # Weighted average
        score = (wind_score * 0.5 + vpd_score * 0.3 + dfm_score * 0.2)
        return np.clip(score, -1, 1)
    
    def _normalize_delta(self, delta: float, max_delta: float) -> float:
        """Normalize delta to -1 to 1 scale"""
        return np.clip(delta / max_delta, -1, 1)
    
    def _calculate_threat_area(self, distance_km: float) -> float:
        """Calculate potential threat area in hectares"""
        # Elliptical fire growth model - CORRECTED
        length_m = distance_km * 1000
        width_m = length_m * 0.4  # Width/length ratio for typical fires
        area_m2 = (length_m * width_m * 3.14159) / 4
        return area_m2 / 10000
    
    def _calculate_arrival_times(self, distance_km: float, lead_time: int) -> List[Dict]:
        """Calculate arrival times at key distances"""
        arrivals = []
        now = datetime.now()
        
        for dist in [1, 2, 5, 10]:
            if distance_km > 0 and dist <= distance_km * 1.5:
                minutes = int((dist / distance_km) * lead_time)
                eta = now + timedelta(minutes=minutes)
                arrivals.append({
                    "distance_km": dist,
                    "eta": eta.strftime("%H:%M"),
                    "minutes": minutes
                })
        
        return arrivals
    
    def _assess_impact(self, distance_km: float) -> Dict:
        """Assess impact level based on spread distance"""
        if distance_km >= 5.0:
            return {"level": "EXTREME", "color": "🔴", "evacuation": "IMMEDIATE"}
        elif distance_km >= 3.0:
            return {"level": "SEVERE", "color": "🟠", "evacuation": "PREPARE"}
        elif distance_km >= 1.5:
            return {"level": "MODERATE", "color": "🟡", "evacuation": "WATCH"}
        else:
            return {"level": "MINOR", "color": "🟢", "evacuation": "MONITOR"}
    
    def _default_trend(self) -> Dict:
        """Default trend when no historical data"""
        return {
            "overall_trend": "🟡 STABLE (Insufficient Data)",
            "escalation_score": 0.0,
            "decision_impact": "USE CAUTION - LIMITED TREND DATA",
            "lead_time_adjustment": 0,
            "trend_multiplier": 1.0,
            "wind": {"delta": 0, "trend": "UNKNOWN", "icon": "?"},
            "vpd": {"delta": 0, "trend": "UNKNOWN", "icon": "?"},
            "dfm": {"delta": 0, "trend": "UNKNOWN", "icon": "?"}
        }
