"""Physical constants and fuel constants"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class PhysicalConstants:
    """Physical constants."""
    HEAT_COMBUSTION = 18000.0
    LATENT_HEAT_VAPORIZATION = 2260.0
    GRAVITY = 9.80665


@dataclass
class FuelConstants:
    """Fuel-specific constants."""
    CRITICAL_LFM: Dict[str, float] = None
    
    def __post_init__(self):
        self.CRITICAL_LFM = {
            "pinus_halepensis": 85.0,
            "quercus_ilex": 90.0,
            "mediterranean_maquis": 80.0,
            "dry_grassland": 70.0
        }


PHYSICAL_CONSTANTS = PhysicalConstants()
FUEL_CONSTANTS = FuelConstants()
