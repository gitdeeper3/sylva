"""Van Wagner crown fire initiation and spread model (1977, 1993)

From SYLVA research paper Section 2.5
"""

class VanWagnerCrownFire:
    """
    Van Wagner's crown fire initiation criteria.
    
    I₀ = (0.010 × CBH × (460 + 25.9 × FMC))^1.5
    """
    
    def __init__(self, fuel_type: str = "pinus_halepensis"):
        self.fuel_type = fuel_type
        self.MIN_CBD_FOR_CROWN = 0.10
    
    def calculate_critical_intensity(self,
                                    canopy_base_height: float,
                                    foliar_moisture: float) -> float:
        """Calculate critical intensity for crown fire initiation (kW/m)."""
        return (0.010 * canopy_base_height * (460 + 25.9 * foliar_moisture)) ** 1.5
    
    def assess_crown_fire_potential(self,
                                   surface_intensity: float,
                                   canopy_base_height: float,
                                   foliar_moisture: float,
                                   canopy_bulk_density: float) -> dict:
        """Assess crown fire potential."""
        I_c = self.calculate_critical_intensity(canopy_base_height, foliar_moisture)
        initiation_possible = surface_intensity >= I_c
        active_spread_possible = canopy_bulk_density >= self.MIN_CBD_FOR_CROWN
        
        if not initiation_possible:
            status = "Surface fire only"
        elif initiation_possible and not active_spread_possible:
            status = "Passive crown fire possible"
        else:
            status = "Active crown fire sustained"
        
        return {
            "crown_fire_status": status,
            "critical_intensity_kW_m": I_c,
            "surface_intensity_kW_m": surface_intensity,
            "initiation_possible": initiation_possible,
            "active_spread_possible": active_spread_possible
        }
