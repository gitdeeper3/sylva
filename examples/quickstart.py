#!/usr/bin/env python3
"""Quick start example for SYLVA framework"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sylva import RapidSpreadForecaster
from sylva.parameters.fuel_moisture import FuelMoistureCalculator
from sylva.utils.fuel_coefficients import FuelCoefficients


def main():
    """Run quick start example."""
    print("=" * 60)
    print("SYLVA - Mediterranean Rapid Fire Spread Forecasting")
    print("=" * 60)
    
    # Initialize forecaster for Pinus halepensis
    forecaster = RapidSpreadForecaster(fuel_type='pinus_halepensis')
    
    # Example parameters from Mati 2018 case study
    print("\n📊 Input Parameters:")
    print("-" * 40)
    print(f"Fuel Type: Pinus halepensis")
    print(f"Live Fuel Moisture (LFM): 65%")
    print(f"Dead Fuel Moisture (DFM): 6%")
    print(f"Canopy Bulk Density (CBD): 0.18 kg/m³")
    print(f"Surface Fuel Load (SFL): 45 tons/ha")
    print(f"Fuel Bed Depth (FBD): 0.8 m")
    print(f"Wind Speed: 10.4 m/s")
    print(f"Vapor Pressure Deficit (VPD): 38.1 hPa")
    print(f"Aspect: 225° (SW)")
    print(f"Drought Code (DC): 487")
    
    # Make prediction
    print("\n🔮 Generating Forecast...")
    print("-" * 40)
    
    result = forecaster.predict(
        lfm=65,
        dfm=6,
        cbd=0.18,
        sfl=45,
        fbd=0.8,
        wind_speed=10.4,
        vpd=38.1,
        aspect=225,
        drought_code=487
    )
    
    # Display results
    print(f"\n✅ Forecast Results:")
    print(f"   Rapid Spread Probability: {result['probability']:.1%}")
    print(f"   Confidence Level: {result['confidence']:.1%}")
    print(f"   Rapid Spread Index (RSI): {result['rsi']:.1f}")
    print(f"   Hazard Level: {result['hazard_level'].upper()}")
    print(f"   Expected Lead Time: {result['lead_time']} minutes")
    
    # Decision support
    print(f"\n🚨 Decision Support:")
    print("-" * 40)
    
    if result['probability'] < 0.2:
        print("   Normal - Routine monitoring")
    elif result['probability'] < 0.4:
        print("   Elevated - Enhanced situational awareness")
    elif result['probability'] < 0.6:
        print("   WATCH - Pre-position resources, public information")
    elif result['probability'] < 0.8:
        print("   WARNING - Resource mobilization, evacuation preparation")
    else:
        print("   IMMINENT - Evacuation execution, full response activation")
    
    # Fuel coefficients
    print(f"\n📚 Fuel Type Information:")
    print("-" * 40)
    fuel_coeff = FuelCoefficients()
    coefficients = fuel_coeff.get_coefficients('pinus_halepensis')
    if coefficients:
        print(f"   Available fuel types: {fuel_coeff.list_fuel_types()}")
        print(f"   Moisture of extinction: {coefficients.moisture_of_extinction:.1%}")
    
    print("\n" + "=" * 60)
    print("SYLVA v0.1.0 - Published: February 12, 2026")
    print("=" * 60)


if __name__ == "__main__":
    main()
