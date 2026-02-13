"""Terrain parameters - Aspect, Slope"""

import numpy as np
from typing import Dict


class TerrainCalculator:
    """Calculate terrain parameters."""
    
    def calculate_aspect_norm(self, aspect: float) -> float:
        """Normalize terrain aspect (0-1)."""
        aspect_rad = np.radians(aspect)
        target_rad = np.radians(225.0)
        norm = (1 + np.cos(aspect_rad - target_rad)) / 2
        return np.clip(norm, 0.0, 1.0)
    
    def get_aspect_class(self, aspect: float) -> Dict:
        """Get aspect class and characteristics."""
        if aspect < 45 or aspect >= 315:
            aspect_class = "N"
            ros_adjustment = 0.8
        elif aspect < 135:
            aspect_class = "E"
            ros_adjustment = 0.9
        elif aspect < 225:
            aspect_class = "S"
            ros_adjustment = 1.2
        else:
            aspect_class = "W"
            ros_adjustment = 1.35
        
        return {
            "aspect_degrees": aspect,
            "aspect_class": aspect_class,
            "ros_adjustment_factor": ros_adjustment,
            "normalized_value": self.calculate_aspect_norm(aspect)
        }
