#!/usr/bin/env python3
"""SYLVA Operational Intelligence Report - Advanced Decision Support"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.abspath('.'))

from sylva_fire.forecasting.rapid_spread_forecast import RapidSpreadForecaster
from sylva_fire.operational.containment_difficulty import ContainmentDifficultyIndex
from sylva_fire.forecasting.crown_fire_probability import CrownFireProbabilityModel
from sylva_fire.forecasting.spread_projection import SpreadDistanceProjector

def generate_operational_report():
    """Generate advanced operational report with all new metrics"""
    
    # Initialize components
    forecaster = RapidSpreadForecaster('pinus_halepensis')
    cdi_calc = ContainmentDifficultyIndex()
    crown_model = CrownFireProbabilityModel()
    spread_proj = SpreadDistanceProjector()
    
    # Mati Fire 2018 parameters
    params = {
        'lfm': 68, 'dfm': 5.1, 'cbd': 0.14, 'sfl': 4.8,
        'fbd': 0.6, 'wind_speed': 10.4, 'vpd': 46.7,
        'aspect': 225, 'drought_code': 487, 'slope': 5
    }
    
    # Get base forecast
    forecast = forecaster.predict(**params)
    
    # Calculate CDI
    cdi = cdi_calc.calculate_cdi(
        ros=forecast['rate_of_spread'],
        flame_length=4.2,  # Calculated from Byram
        fuel_type='pinus_halepensis',
        slope=5,
        wind_speed=10.4,
        fuel_continuity=0.85
    )
    
    # Calculate crown fire probability
    crown = crown_model.calculate_crown_fire_probability(
        surface_intensity=8200,  # kW/m from Byram
        canopy_bulk_density=0.14,
        canopy_base_height=4.0,
        foliar_moisture=68,
        wind_speed=10.4,
        fuel_type='pinus_halepensis'
    )
    
    # Calculate spread projection
    spread = spread_proj.calculate_potential_spread(
        ros=forecast['rate_of_spread'],
        wind_speed=10.4,
        wind_direction=225,
        slope=5,
        slope_aspect=225,
        lead_time=90,
        fuel_continuity=0.85
    )
    
    # Print operational report
    print("\n" + "=" * 80)
    print("🔥 SYLVA OPERATIONAL INTELLIGENCE - ADVANCED DECISION SUPPORT")
    print("=" * 80)
    
    print(f"\n📊 RAPID SPREAD FORECAST")
    print(f"   Probability: {forecast['probability']:.1%}")
    print(f"   RSI: {forecast['rsi']:.3f}")
    print(f"   ROS: {forecast['rate_of_spread']:.1f} m/min")
    
    print(f"\n🛡️ CONTAINMENT DIFFICULTY")
    print(f"   CDI Score: {cdi['cdi_score']}/100 - {cdi['cdi_color']} {cdi['cdi_level']}")
    print(f"   Handline: {cdi['handline_feasibility']}")
    print(f"   Dozer: {cdi['dozer_feasibility']}")
    print(f"   Aerial: {cdi['aerial_effectiveness']}")
    print(f"   Tactic: {cdi['recommended_tactic']}")
    
    print(f"\n🌲 CROWN FIRE POTENTIAL")
    print(f"   Initiation Probability: {crown['crown_fire_initiation_probability']:.1%}")
    print(f"   Spread Probability: {crown['crown_fire_spread_probability']:.1%}")
    print(f"   Type: {crown['crown_fire_color']} {crown['crown_fire_type']}")
    print(f"   Spotting: {crown['spotting_potential']}")
    
    print(f"\n📍 SPREAD PROJECTION (90 minutes)")
    print(f"   Head Fire: {spread['head_fire_distance_km']} km")
    print(f"   Flank Fire: {spread['flank_fire_distance_km']} km")
    print(f"   Impact Radius: {spread['impact_radius_km']} km")
    print(f"   Potential Area: {spread['potential_burned_area_ha']} ha")
    print(f"   Wind-Slope Alignment: {spread['alignment_category']}")
    
    print(f"\n🚨 EVACUATION & RESOURCE REQUIREMENTS")
    resources = cdi_calc.get_suppression_resources(cdi['cdi_score'], spread['potential_burned_area_ha'])
    print(f"   Hand Crews Required: {resources['hand_crews']}")
    print(f"   Fire Engines: {resources['fire_engines']}")
    print(f"   Air Tankers: {resources['air_tankers']}")
    print(f"   Dozers: {resources['dozers']}")
    
    print(f"\n⏱️  ARRIVAL TIMES")
    for arrival in spread['arrival_times']:
        print(f"   {arrival['distance_km']} km: {arrival['estimated_arrival']} "
              f"({arrival['minutes_from_now']:.0f} min)")
    
    print("\n" + "=" * 80)
    print("✅ SYLVA Operational Intelligence Complete")
    print("=" * 80)
    
    return {
        'forecast': forecast,
        'cdi': cdi,
        'crown': crown,
        'spread': spread,
        'resources': resources
    }

if __name__ == "__main__":
    generate_operational_report()
