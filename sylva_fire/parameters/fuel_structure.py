"""Fuel structure parameters - CBD, CBH, SFL, FBD"""

from typing import Dict


class FuelStructureCalculator:
    """Calculate fuel structure parameters."""
    
    def __init__(self, fuel_type: str = "pinus_halepensis"):
        self.fuel_type = fuel_type
    
    def classify_cbd_hazard(self, cbd: float) -> Dict:
        """Classify CBD hazard level."""
        if cbd < 0.05:
            level = "Very Low"
        elif cbd < 0.10:
            level = "Low"
        elif cbd < 0.15:
            level = "Moderate"
        elif cbd < 0.25:
            level = "High"
        else:
            level = "Extreme"
        
        return {
            "cbd_kg_m3": cbd,
            "hazard_level": level
        }
    
    def get_fuel_defaults(self, fuel_type: str = None) -> Dict:
        """Get default fuel structure parameters."""
        if fuel_type is None:
            fuel_type = self.fuel_type
        
        defaults = {
            "pinus_halepensis": {
                "cbd_typical": 0.15,
                "cbh_typical": 4.0,
                "sfl_typical": 25.0,
                "fbd_typical": 0.6
            },
            "quercus_ilex": {
                "cbd_typical": 0.18,
                "cbh_typical": 3.0,
                "sfl_typical": 35.0,
                "fbd_typical": 0.7
            },
            "mediterranean_maquis": {
                "cbd_typical": 0.30,
                "cbh_typical": 1.2,
                "sfl_typical": 45.0,
                "fbd_typical": 2.5
            },
            "dry_grassland": {
                "cbd_typical": 0.0,
                "cbh_typical": 0.0,
                "sfl_typical": 4.0,
                "fbd_typical": 0.5
            }
        }
        
        return defaults.get(fuel_type, defaults["pinus_halepensis"])

    # Add Pinus pinaster to fuel defaults
    def _add_pinus_pinaster(self):
        """Add Pinus pinaster fuel parameters"""
        self.params["pinus_pinaster"] = {
            "net_fuel_load": 3.0,
            "surface_area_volume": 3200.0,
            "fuel_bed_depth": 0.7,
            "moisture_of_extinction": 0.22,
            "heat_content": 18500.0,
            "ovendry_density": 540.0,
            "particle_density": 1540.0,
            "optimum_packing_ratio": 0.019
        }
        
        self.RSI_WEIGHTS["pinus_pinaster"] = {
            "lfm": 0.19, "dfm": 0.16, "cbd": 0.13, "sfl": 0.11,
            "fbd": 0.09, "wind": 0.16, "vpd": 0.08, "aspect": 0.05, "dc": 0.06
        }
        
        self.CALIBRATION_COEFFS["pinus_pinaster"] = {
            "beta_0": -4.6, "beta_1": 8.9, "beta_2": -3.9, "beta_3": 1.35
        }
