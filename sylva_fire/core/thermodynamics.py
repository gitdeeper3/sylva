"""Thermodynamic continuum model - Section 2.1"""

class ThermodynamicContinuum:
    """
    Thermodynamic formulation: Fuel complex as heat-moisture continuum
    """
    
    def __init__(self):
        self.LATENT_HEAT_VAPORIZATION = 2260.0
    
    def calculate_energy_balance(self,
                                flame_heat_release: float,
                                fuel_moisture: float = 10.0) -> dict:
        """Calculate simplified energy balance."""
        Q_preheat = 250.0 + 1116.0 * (fuel_moisture / 100.0)
        Q_vaporization = self.LATENT_HEAT_VAPORIZATION * (fuel_moisture / 100.0)
        Q_pyrolysis = 1500.0
        
        total_sink = Q_preheat + Q_pyrolysis + Q_vaporization
        
        return {
            "flame_heat_release_kW": flame_heat_release,
            "total_heat_sink_kJ_kg": total_sink,
            "energy_balance_ratio": flame_heat_release / total_sink if total_sink > 0 else 0
        }
