"""Fuel-type specific coefficients"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class FuelCoefficientSet:
    """Coefficient set for a specific fuel type."""
    weight_lfm: float = 0.20
    weight_dfm: float = 0.15
    weight_cbd: float = 0.12
    weight_sfl: float = 0.10
    weight_fbd: float = 0.08
    weight_wind: float = 0.15
    weight_vpd: float = 0.08
    weight_aspect: float = 0.06
    weight_dc: float = 0.06


class FuelCoefficients:
    """Manager for fuel-type specific coefficients."""
    
    _instance = None
    _coefficients: Dict[str, FuelCoefficientSet] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FuelCoefficients, cls).__new__(cls)
            cls._instance._load_coefficients()
        return cls._instance
    
    def _load_coefficients(self):
        """Load default coefficients."""
        self._coefficients["pinus_halepensis"] = FuelCoefficientSet(
            weight_lfm=0.20, weight_dfm=0.15, weight_cbd=0.12,
            weight_sfl=0.10, weight_fbd=0.08, weight_wind=0.15,
            weight_vpd=0.08, weight_aspect=0.06, weight_dc=0.06
        )
        self._coefficients["quercus_ilex"] = FuelCoefficientSet(
            weight_lfm=0.18, weight_dfm=0.14, weight_cbd=0.14,
            weight_sfl=0.12, weight_fbd=0.10, weight_wind=0.14,
            weight_vpd=0.07, weight_aspect=0.05, weight_dc=0.06
        )
        self._coefficients["mediterranean_maquis"] = FuelCoefficientSet(
            weight_lfm=0.22, weight_dfm=0.16, weight_cbd=0.10,
            weight_sfl=0.08, weight_fbd=0.06, weight_wind=0.16,
            weight_vpd=0.09, weight_aspect=0.07, weight_dc=0.06
        )
        self._coefficients["dry_grassland"] = FuelCoefficientSet(
            weight_lfm=0.15, weight_dfm=0.18, weight_cbd=0.08,
            weight_sfl=0.12, weight_fbd=0.10, weight_wind=0.18,
            weight_vpd=0.10, weight_aspect=0.04, weight_dc=0.05
        )
    
    def get_coefficients(self, fuel_type: str) -> Optional[FuelCoefficientSet]:
        """Get coefficients for specified fuel type."""
        return self._coefficients.get(fuel_type)
    
    def list_fuel_types(self) -> list:
        """List all available fuel types."""
        return list(self._coefficients.keys())
