#!/usr/bin/env python3
"""SYLVA Tactical Decision Dashboard - Advanced Operational Intelligence"""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sylva_fire.forecasting.rapid_spread_forecast import RapidSpreadForecaster
from sylva_fire.forecasting.escalation_trend import EscalationTrendAnalyzer
from sylva_fire.operational.containment_strategy import ContainmentStrategyEngine
from sylva_fire.forecasting.crown_fire_probability import CrownFireProbabilityModel

def generate_tactical_dashboard():
    """Generate complete tactical decision dashboard"""
    
    # Initialize components
    forecaster = RapidSpreadForecaster('pinus_halepensis')
    trend_analyzer = EscalationTrendAnalyzer()
    containment_engine = ContainmentStrategyEngine()
    crown_model = CrownFireProbabilityModel()
    
    # Mati Fire 2018 parameters
    current_params = {
        'lfm': 68, 'dfm': 5.1, 'cbd': 0.14, 'sfl': 4.8,
        'fbd': 0.6, 'wind_speed': 10.4, 'vpd': 46.7,
        'aspect': 225, 'drought_code': 487, 'slope': 5
    }
    
    # Historical data for trend analysis (last 3 hours)
    historical_hourly = [
        {'wind_speed': 8.9, 'vpd': 42.3, 'dfm': 5.4},
        {'wind_speed': 9.8, 'vpd': 44.5, 'dfm': 5.2},
        {'wind_speed': 10.2, 'vpd': 45.8, 'dfm': 5.1},
    ]
    
    # Get base forecast
    forecast = forecaster.predict(**current_params)
    
    # Analyze trends
    trends = trend_analyzer.analyze_trends(current_params, historical_hourly)
    
    # Project spread distance
    spread = trend_analyzer.project_spread_distance(
        ros=forecast['rate_of_spread'],
        lead_time=90,
        wind_trend=trends['overall_trend'],
        terrain_factor=1.2
    )
    
    # Assess containment
    containment = containment_engine.assess_containment(
        ros=forecast['rate_of_spread'],
        flame_length=4.2,
        fuel_type='pinus_halepensis',
        wind_speed=current_params['wind_speed'],
        slope=current_params['slope'],
        wui_proximity_km=1.5,
        access_difficulty=0.4
    )
    
    # Crown fire probability
    crown = crown_model.calculate_crown_fire_probability(
        surface_intensity=8200,
        canopy_bulk_density=current_params['cbd'],
        canopy_base_height=4.0,
        foliar_moisture=current_params['lfm'],
        wind_speed=current_params['wind_speed'],
        fuel_type='pinus_halepensis'
    )
    
    # ============ TACTICAL DASHBOARD ============
    print("\n" + "╔" + "═" * 98 + "╗")
    print("║🔥 SYLVA TACTICAL DECISION DASHBOARD - ADVANCED OPERATIONAL INTELLIGENCE║")
    print("╚" + "═" * 98 + "╝")
    
    print(f"\n📍 LOCATION: Attica, Greece | WUI Distance: 1.5 km")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | DOI: 10.5281/zenodo.18627186")
    
    # 1. ESCALATION TREND
    print("\n" + "┌" + "─" * 98 + "┐")
    print("│ 🔥 FIRE ENVIRONMENT TREND (Last 3 Hours)                          │")
    print("├" + "─" * 98 + "┤")
    print(f"│ Wind:  {trends['wind']['icon']} {trends['wind']['trend']:25s} "
          f"(Δ{trends['wind']['delta']:+0.1f} m/s)            │")
    print(f"│ VPD:   {trends['vpd']['icon']} {trends['vpd']['trend']:25s} "
          f"(Δ{trends['vpd']['delta']:+0.1f} hPa)            │")
    print(f"│ DFM:   {trends['dfm']['icon']} {trends['dfm']['trend']:25s} "
          f"(Δ{trends['dfm']['delta']:+0.1f}%)             │")
    print(f"│                                                                    │")
    print(f"│ OVERALL: {trends['overall_trend']:40s}              │")
    print(f"│ DECISION: {trends['decision_impact']:46s}│")
    print("└" + "─" * 98 + "┘")
    
    # 2. SPREAD PROJECTION
    print("\n" + "┌" + "─" * 98 + "┐")
    print("│ 📍 FIRE SPREAD PROJECTION (90 Minutes)                           │")
    print("├" + "─" * 98 + "┤")
    print(f"│ Head Fire Distance: {spread['projected_distance_km']:4.1f} km "
          f"(Range: {spread['distance_range_km']['min']}-{spread['distance_range_km']['max']} km)      │")
    print(f"│ Threat Zone Area:   {spread['threat_zone_ha']:6.1f} ha                                     │")
    print(f"│ Evacuation Buffer:  {spread['evacuation_buffer_km']:4.1f} km                                     │")
    print(f"│ Impact Level:       {spread['impact_assessment']['color']} {spread['impact_assessment']['level']:8s} - "
          f"{spread['impact_assessment']['evacuation']}                               │")
    print("├" + "─" * 98 + "┤")
    print("│ ETA to Key Distances:                                            │")
    for eta in spread['arrival_times'][:3]:
        print(f"│   • {eta['distance_km']:2d} km: {eta['eta']} ({eta['minutes']} min)                                      │")
    print("└" + "─" * 98 + "┘")
    
    # 3. CONTAINMENT DIFFICULTY
    print("\n" + "┌" + "─" * 98 + "┐")
    print("│ 🛡️  CONTAINMENT DIFFICULTY ASSESSMENT                            │")
    print("├" + "─" * 98 + "┤")
    print(f"│ Difficulty: {containment['containment_difficulty']['color']} "
          f"{containment['containment_difficulty']['class']:17s} "
          f"(Score: {containment['containment_difficulty']['score']:.2f})                    │")
    print(f"│ Initial Attack:  {containment['initial_attack_feasibility']:35s}      │")
    print(f"│ Est. Containment: {containment['estimated_containment_time_hr']:3.1f} hours "
          f"(Success: {containment['containment_success_probability']:.0%})                      │")
    print("├" + "─" * 98 + "┤")
    print("│ Critical Factors:                                                │")
    for factor in containment['critical_factors']:
        print(f"│   • {factor:50s}          │")
    print("├" + "─" * 98 + "┤")
    print("│ RESOURCE REQUIREMENTS:                                           │")
    res = containment['resource_recommendations']
    print(f"│   Hand Crews: {res['hand_crews']:3d}     Fire Engines: {res['fire_engines']:3d}     "
          f"Air Tankers: {res['air_tankers']:1d}     Helicopters: {res['helicopters']:1d}     │")
    print(f"│   Dozers: {res['dozers']:3d}        Overhead: {res['overhead']:7s}                              │")
    print("└" + "─" * 98 + "┘")
    
    # 4. CROWN FIRE & WUI THREAT
    print("\n" + "┌" + "─" * 98 + "┐")
    print("│ 🌲 CROWN FIRE & WUI THREAT ASSESSMENT                           │")
    print("├" + "─" * 98 + "┤")
    print(f"│ Crown Fire Initiation: {crown['crown_fire_initiation_probability']:.1%}                              │")
    print(f"│ Crown Fire Type:       {crown['crown_fire_color']} {crown['crown_fire_type']:30s}           │")
    print(f"│ Spotting Potential:    {crown['spotting_potential']:35s}      │")
    print("├" + "─" * 98 + "┤")
    print(f"│ WUI Threat Level:      {containment['wui_assessment']['color']} {containment['wui_assessment']['threat_level']:8s} - "
          f"{containment['wui_assessment']['evacuation_status']} EVACUATION                   │")
    print(f"│ Structures at Risk:    {containment['wui_assessment']['structure_threat_count']}                                    │")
    print(f"│ Est. Fire Arrival:     {containment['wui_assessment']['estimated_arrival_min']:.0f} minutes                              │")
    print("└" + "─" * 98 + "┘")
    
    # 5. STRATEGIC RECOMMENDATION
    print("\n" + "┌" + "─" * 98 + "┐")
    print("│ 🎯 STRATEGIC DECISION SUPPORT                                   │")
    print("├" + "─" * 98 + "┤")
    print(f"│ Strategic Priority: {containment['strategic_priority']:60s} │")
    print("├" + "─" * 98 + "┤")
    print("│ IMMEDIATE ACTIONS:                                               │")
    print("│   1. ACTIVATE Type 2 Incident Management Team                    │")
    print("│   2. PRE-POSITION aerial resources within 5 km                   │")
    print("│   3. INITIATE pre-evacuation warning for coastal areas           │")
    print("│   4. DEPLOY additional hand crews for structure protection       │")
    print("│   5. COORDINATE with neighboring jurisdictions                   │")
    print("└" + "─" * 98 + "┘")
    
    print("\n" + "═" * 100)
    print("✅ SYLVA Tactical Dashboard Complete - Decision Superiority Achieved")
    print("═" * 100 + "\n")
    
    return {
        'forecast': forecast,
        'trends': trends,
        'spread': spread,
        'containment': containment,
        'crown': crown
    }

if __name__ == "__main__":
    generate_tactical_dashboard()
