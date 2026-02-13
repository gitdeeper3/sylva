"""Byram's fireline intensity model (1959)

From SYLVA research paper Section 2.3
"""

class ByramIntensity:
    """
    Byram's fireline intensity (kW/m)
    
    I = H × w × R
    """
    
    def __init__(self):
        pass
    
    def calculate_intensity(self,
                           heat_content: float,
                           fuel_consumed: float,
                           rate_of_spread: float) -> float:
        """Calculate Byram fireline intensity."""
        return heat_content * fuel_consumed * rate_of_spread
    
    def flame_length_from_intensity(self, intensity: float) -> float:
        """Calculate flame length from Byram intensity."""
        return 0.0775 * (intensity ** 0.46)
    
    def get_fire_behavior_class(self, intensity: float) -> dict:
        """Classify fire behavior based on Byram intensity."""
        if intensity < 500:
            class_name = "Low"
        elif intensity < 2000:
            class_name = "Moderate"
        elif intensity < 4000:
            class_name = "High"
        elif intensity < 10000:
            class_name = "Very High"
        elif intensity < 25000:
            class_name = "Extreme"
        else:
            class_name = "Catastrophic"
        
        return {
            "intensity_kW_m": intensity,
            "class": class_name,
            "flame_length_m": self.flame_length_from_intensity(intensity)
        }
