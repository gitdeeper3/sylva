"""Forecasting modules"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sylva_fire.forecasting.rapid_spread_forecast import RapidSpreadForecaster

__all__ = [
    "RapidSpreadForecaster",
]
