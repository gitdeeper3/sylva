#!/usr/bin/env python3
"""SYLVA - Rapid Fire Spread Forecast Runner"""

import sys
import os
import json
from datetime import datetime

# Add project path
sys.path.insert(0, os.path.abspath('.'))

try:
    from sylva_fire.forecasting.rapid_spread_forecast import RapidSpreadForecaster
    from sylva_fire.parameters.fuel_moisture import FuelMoistureCalculator
    from sylva_fire.parameters.terrain import TerrainCalculator
    from sylva_fire.integration.rsi_calculator import RSICalculator
    print("✅ SYLVA modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def run_mati_case():
    """Run Mati Fire 2018 case study"""
    print("\n" + "="*60)
    print("🔥 SYLVA RAPID SPREAD FORECAST - MATI FIRE 2018")
    print("="*60)
    
    # Initialize forecaster
    forecaster = RapidSpreadForecaster(fuel_type='pinus_halepensis')
    
    # Parameters 60 minutes before rapid spread onset (16:00 LST)
    params = {
        'lfm': 68,           # Live Fuel Moisture (%)
        'dfm': 5.1,          # Dead Fuel Moisture (%)
        'cbd': 0.14,         # Canopy Bulk Density (kg/m³)
        'sfl': 4.8,          # Surface Fuel Load (tons/ha)
        'fbd': 0.6,          # Fuel Bed Depth (m)
        'wind_speed': 10.4,  # Wind speed (m/s)
        'vpd': 46.7,         # Vapor Pressure Deficit (hPa)
        'aspect': 225,       # Aspect (degrees SW)
        'drought_code': 487  # Drought Code
    }
    
    print("\n📊 INPUT PARAMETERS:")
    print("-"*40)
    for key, value in params.items():
        print(f"  {key:12s}: {value}")
    
    # Run forecast
    print("\n🔄 Generating forecast...")
    result = forecaster.predict(**params)
    
    # Display results
    print("\n✅ FORECAST RESULTS:")
    print("-"*40)
    print(f"  Rapid Spread Probability: {result['probability']:.1%}")
    print(f"  Confidence Level:        {result['confidence']:.1%}")
    print(f"  Rapid Spread Index (RSI): {result['rsi']:.3f}")
    print(f"  Hazard Level:            {result['hazard_level'].upper()}")
    print(f"  Lead Time:              {result['lead_time']} minutes")
    print(f"  Rate of Spread:         {result['rate_of_spread']:.1f} m/min")
    
    # Decision support
    decision = forecaster.get_decision_support(result['probability'])
    print("\n🚨 DECISION SUPPORT:")
    print("-"*40)
    print(f"  Action: {decision['action']}")
    print(f"  Public Message: {decision['public_message']}")
    
    # Parameter contributions
    print("\n📈 PARAMETER CONTRIBUTIONS:")
    print("-"*40)
    contributions = result['parameter_contributions']
    for param, contrib in sorted(contributions.items(), key=lambda x: x[1], reverse=True):
        print(f"  {param.upper():6s}: {contrib:.1%}")
    
    return result

def run_sensitivity_analysis():
    """Run sensitivity analysis on key parameters"""
    print("\n" + "="*60)
    print("📊 SENSITIVITY ANALYSIS")
    print("="*60)
    
    forecaster = RapidSpreadForecaster('pinus_halepensis')
    base_params = {
        'lfm': 68, 'dfm': 5.1, 'cbd': 0.14, 'sfl': 4.8,
        'fbd': 0.6, 'wind_speed': 10.4, 'vpd': 46.7,
        'aspect': 225, 'drought_code': 487
    }
    
    # Test DFM sensitivity
    print("\nDFM Sensitivity:")
    print("-"*20)
    for dfm in [4, 6, 8, 10, 12, 15]:
        params = base_params.copy()
        params['dfm'] = dfm
        result = forecaster.predict(**params)
        print(f"  DFM = {dfm:2d}% → Probability = {result['probability']:.1%}")
    
    # Test wind sensitivity
    print("\nWind Speed Sensitivity:")
    print("-"*20)
    for wind in [5, 8, 10, 12, 15, 20]:
        params = base_params.copy()
        params['wind_speed'] = wind
        result = forecaster.predict(**params)
        print(f"  Wind = {wind:2d} m/s → Probability = {result['probability']:.1%}")

def run_batch_forecast():
    """Run batch forecast for multiple scenarios"""
    print("\n" + "="*60)
    print("📋 BATCH FORECAST - MULTIPLE SCENARIOS")
    print("="*60)
    
    forecaster = RapidSpreadForecaster('pinus_halepensis')
    
    scenarios = [
        {"name": "Normal Conditions", "lfm": 120, "dfm": 15, "wind_speed": 5},
        {"name": "Moderate Risk", "lfm": 90, "dfm": 10, "wind_speed": 8},
        {"name": "High Risk", "lfm": 70, "dfm": 7, "wind_speed": 12},
        {"name": "Extreme - Mati 2018", "lfm": 68, "dfm": 5.1, "wind_speed": 10.4},
        {"name": "Catastrophic", "lfm": 50, "dfm": 4, "wind_speed": 15}
    ]
    
    print("\n{:<25} {:>15} {:>15} {:>15}".format(
        "Scenario", "DFM(%)", "Wind(m/s)", "Probability"))
    print("-"*70)
    
    for scenario in scenarios:
        params = {
            'lfm': scenario['lfm'],
            'dfm': scenario['dfm'],
            'cbd': 0.14,
            'sfl': 4.8,
            'fbd': 0.6,
            'wind_speed': scenario['wind_speed'],
            'vpd': 38,
            'aspect': 225,
            'drought_code': 400
        }
        result = forecaster.predict(**params)
        print("{:<25} {:>15.1f} {:>15.1f} {:>14.1%}".format(
            scenario['name'], 
            scenario['dfm'], 
            scenario['wind_speed'], 
            result['probability']
        ))

if __name__ == "__main__":
    print("\n🔥 SYLVA v1.0.0 - Mediterranean Rapid Fire Spread Forecasting")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📋 DOI: 10.5281/zenodo.18627186")
    
    # Run Mati case study
    result = run_mati_case()
    
    # Run sensitivity analysis
    run_sensitivity_analysis()
    
    # Run batch forecast
    run_batch_forecast()
    
    print("\n" + "="*60)
    print("✅ Forecast completed successfully")
    print("="*60)
