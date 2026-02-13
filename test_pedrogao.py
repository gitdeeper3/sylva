#!/usr/bin/env python3
"""Test Pedrógão Grande 2017 case study"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from sylva_fire.forecasting.rapid_spread_forecast import RapidSpreadForecaster

print("\n🔥 Pedrógão Grande 2017 - Portugal")
print("="*50)

forecaster = RapidSpreadForecaster('pinus_pinaster')

params = {
    'lfm': 72,
    'dfm': 6.1,
    'cbd': 0.21,
    'sfl': 28,
    'fbd': 0.8,
    'wind_speed': 13.4,
    'vpd': 48.2,
    'aspect': 180,
    'drought_code': 487
}

result = forecaster.predict(**params)

print(f"\n📊 60-min lead time:")
print(f"   Probability: {result['probability']:.1%}")
print(f"   RSI: {result['rsi']:.3f}")
print(f"   Hazard: {result['hazard_level'].upper()}")
print(f"   ROS: {result['rate_of_spread']:.1f} m/min")
