"""Utility modules"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sylva_fire.utils.fuel_coefficients import FuelCoefficients

__all__ = [
    "FuelCoefficients",
]
