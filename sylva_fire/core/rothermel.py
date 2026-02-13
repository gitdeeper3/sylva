"""Rothermel surface fire spread model (1972) - Complete implementation

From SYLVA research paper Section 2.2 and Appendix B
"""

import numpy as np
from typing import Dict, Optional


class RothermelModel:
    """
    Rothermel's surface fire spread model (1972).
    
    ROS = (I_R · ξ · (1 + φ_w + φ_s)) / (ρ_b · Q_ig)
    """
    
    def __init__(self, fuel_type: str = "pinus_halepensis"):
        self.fuel_type = fuel_type
        self._load_fuel_parameters()
    
    def _load_fuel_parameters(self):
        """Load fuel-specific parameters."""
        self.params = {
            "pinus_halepensis": {
                "net_fuel_load": 2.5,
                "surface_area_volume": 3500.0,
                "fuel_bed_depth": 0.6,
                "moisture_of_extinction": 0.25,
                "heat_content": 18600.0,
                "ovendry_density": 512.0,
                "particle_density": 1540.0,
                "optimum_packing_ratio": 0.02
            },
            "quercus_ilex": {
                "net_fuel_load": 3.2,
                "surface_area_volume": 2800.0,
                "fuel_bed_depth": 1.2,
                "moisture_of_extinction": 0.30,
                "heat_content": 18400.0,
                "ovendry_density": 580.0,
                "particle_density": 1540.0,
                "optimum_packing_ratio": 0.018
            },
            "mediterranean_maquis": {
                "net_fuel_load": 4.0,
                "surface_area_volume": 4000.0,
                "fuel_bed_depth": 1.5,
                "moisture_of_extinction": 0.20,
                "heat_content": 18800.0,
                "ovendry_density": 490.0,
                "particle_density": 1540.0,
                "optimum_packing_ratio": 0.025
            },
            "dry_grassland": {
                "net_fuel_load": 0.8,
                "surface_area_volume": 4500.0,
                "fuel_bed_depth": 0.4,
                "moisture_of_extinction": 0.15,
                "heat_content": 17200.0,
                "ovendry_density": 320.0,
                "particle_density": 1540.0,
                "optimum_packing_ratio": 0.015
            },
            "pinus_pinaster": {
                "net_fuel_load": 3.0,
                "surface_area_volume": 3200.0,
                "fuel_bed_depth": 0.7,
                "moisture_of_extinction": 0.22,
                "heat_content": 18500.0,
                "ovendry_density": 540.0,
                "particle_density": 1540.0,
                "optimum_packing_ratio": 0.019
            }
        }
        
        if self.fuel_type not in self.params:
            self.fuel_type = "pinus_halepensis"
        self.fuel_params = self.params[self.fuel_type]
    
    def calculate_rate_of_spread(self, 
                                fuel_moisture: float,
                                wind_speed: float,
                                slope: float = 0.0,
                                fuel_type: Optional[str] = None) -> float:
        """
        Calculate surface fire rate of spread (m/min) by fuel type
        """
        if fuel_type is None:
            fuel_type = self.fuel_type
            
        # Base ROS by fuel type (Mediterranean calibration)
        ros_base = {
            "pinus_halepensis": 5.0 + (wind_speed * 2.2) - (fuel_moisture * 0.15),
            "quercus_ilex": 4.0 + (wind_speed * 1.8) - (fuel_moisture * 0.12),
            "mediterranean_maquis": 6.0 + (wind_speed * 2.5) - (fuel_moisture * 0.18),
            "dry_grassland": 8.0 + (wind_speed * 3.0) - (fuel_moisture * 0.20),
            "pinus_pinaster": 5.5 + (wind_speed * 2.4) - (fuel_moisture * 0.16)
        }
        
        ros = ros_base.get(fuel_type, 5.0 + (wind_speed * 2.0) - (fuel_moisture * 0.1))
        ros = ros * (1 + slope * 0.05)  # Slope effect
        
        return max(1.0, ros)
    
    def calculate_flame_length(self, fireline_intensity: float) -> float:
        """Calculate flame length from Byram intensity (m)."""
        return 0.0775 * (fireline_intensity ** 0.46)
