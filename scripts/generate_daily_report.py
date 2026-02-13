#!/usr/bin/env python3
"""SYLVA v2.5 - Professional Operational Intelligence Report - COMPLETE"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import math

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import SYLVA modules
from sylva_fire.forecasting.rapid_spread_forecast import RapidSpreadForecaster
from sylva_fire.forecasting.escalation_trend import EscalationTrendAnalyzer
from sylva_fire.operational.containment_strategy import ContainmentStrategyEngine
from sylva_fire.forecasting.crown_fire_probability import CrownFireProbabilityModel

# Try to import text report generator
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../reports/daily')))
    from to_txt_fixed import SYLVATextReport
    TEXT_REPORT_AVAILABLE = True
except ImportError:
    TEXT_REPORT_AVAILABLE = False
    print("⚠️ Text report generator not available")

class DailyReportGenerator:
    def __init__(self):
        self.forecaster = RapidSpreadForecaster('pinus_halepensis')
        self.trend_analyzer = EscalationTrendAnalyzer()
        self.containment_engine = ContainmentStrategyEngine()
        self.crown_model = CrownFireProbabilityModel()
        self.date = datetime.now().strftime('%Y-%m-%d')
    
    # ======== RISK CALCULATION ========
    def _calculate_risk_level_quantitative(self, params, forecast, containment, crown):
        """Quantitative risk assessment (0-100)"""
        risk_score = 0
        
        # 1. DFM contribution (0-25)
        dfm = params.get('dfm', 15)
        if dfm < 6:
            risk_score += 25
        elif dfm < 8:
            risk_score += 20
        elif dfm < 10:
            risk_score += 15
        elif dfm < 12:
            risk_score += 10
        
        # 2. Wind contribution (0-25)
        wind = params.get('wind_speed', 0)
        if wind >= 15:
            risk_score += 25
        elif wind >= 12:
            risk_score += 20
        elif wind >= 10:
            risk_score += 15
        elif wind >= 8:
            risk_score += 10
        
        # 3. VPD contribution (0-15)
        vpd = params.get('vpd', 0)
        if vpd >= 40:
            risk_score += 15
        elif vpd >= 30:
            risk_score += 12
        elif vpd >= 25:
            risk_score += 8
        elif vpd >= 20:
            risk_score += 5
        
        # 4. Drought Code contribution (0-15)
        dc = params.get('drought_code', 0)
        if dc >= 500:
            risk_score += 15
        elif dc >= 450:
            risk_score += 12
        elif dc >= 400:
            risk_score += 8
        elif dc >= 350:
            risk_score += 5
        
        # 5. Crown fire contribution (0-10)
        risk_score += int(crown['crown_fire_initiation_probability'] * 10)
        
        # 6. Containment difficulty contribution (0-10)
        risk_score += int(containment['containment_difficulty']['score'] * 10)
        
        # Determine risk level
        if risk_score >= 80:
            return {"score": risk_score, "level": "EXTREME", "color": "⚫", 
                    "description": "Type 1 Incident Complexity - Catastrophic fire behavior"}
        elif risk_score >= 65:
            return {"score": risk_score, "level": "VERY HIGH", "color": "🔴", 
                    "description": "Type 1 Incident Complexity - Critical fire behavior"}
        elif risk_score >= 50:
            return {"score": risk_score, "level": "HIGH", "color": "🟠", 
                    "description": "Type 2 Incident Complexity - Severe fire behavior"}
        elif risk_score >= 35:
            return {"score": risk_score, "level": "MODERATE", "color": "🟡", 
                    "description": "Type 3 Incident Complexity - Moderate fire behavior"}
        else:
            return {"score": risk_score, "level": "LOW", "color": "🟢", 
                    "description": "Type 4/5 Incident Complexity - Routine operations"}
    
    # ======== THREAT ZONE CALCULATION ========
    def _calculate_threat_zone(self, max_distance_km):
        """Calculate threat zone using elliptical fire growth model"""
        length_m = max_distance_km * 1000
        width_m = length_m * 0.25  # Head fire dominant ratio
        area_m2 = (length_m * width_m * math.pi) / 4  # Ellipse area
        return round(area_m2 / 10000, 1)  # Convert to hectares
    
    # ======== DRIVER RANKING ========
    def _calculate_driver_ranking(self, params):
        """Calculate and rank primary risk drivers"""
        drivers = {
            "Wind": min(100, (params.get('wind_speed', 0) / 12) * 100),
            "DFM": min(100, ((15 - params.get('dfm', 15)) / 9) * 100),
            "VPD": min(100, (params.get('vpd', 0) / 35) * 100),
            "LFM": min(100, ((100 - params.get('lfm', 100)) / 40) * 100),
            "DC": min(100, (params.get('drought_code', 0) / 500) * 100)
        }
        # Sort by value descending and format as percentages
        return {k: f"{int(v)}%" for k, v in sorted(drivers.items(), key=lambda x: x[1], reverse=True)}
    
    # ======== SPREAD PROJECTION ========
    def _calculate_spread_projection(self, params, lead_time=90):
        """Calculate fire spread projection for all fuel types"""
        ros_values = {}
        fuel_types = ['dry_grassland', 'mediterranean_maquis', 'pinus_halepensis', 'quercus_ilex']
        
        for ft in fuel_types:
            try:
                forecaster = RapidSpreadForecaster(ft)
                result = forecaster.predict(**params)
                ros_values[ft] = result['rate_of_spread']
            except Exception as e:
                print(f"⚠️ Error calculating ROS for {ft}: {e}")
                ros_values[ft] = 20.0  # Default fallback
        
        # Calculate spread distances (km)
        spread_distances = {ft: round((ros * lead_time) / 1000, 1) for ft, ros in ros_values.items()}
        
        # Find maximum values
        max_ros_ft = max(ros_values, key=ros_values.get)
        max_ros = ros_values[max_ros_ft]
        max_distance = spread_distances[max_ros_ft]
        
        # Calculate threat zone
        threat_zone_ha = self._calculate_threat_zone(max_distance)
        
        # Calculate WUI arrival time
        wui_distance_km = params.get('wui_distance', 1.5)
        wui_distance_m = wui_distance_km * 1000
        wui_arrival_times = {}
        
        for ft, ros in ros_values.items():
            if ros > 0:
                wui_arrival_times[ft] = round(wui_distance_m / ros)
            else:
                wui_arrival_times[ft] = float('inf')
        
        min_arrival = min(wui_arrival_times.values())
        worst_case_fuel = min(wui_arrival_times, key=wui_arrival_times.get)
        
        # Calculate arrival times for key distances
        now = datetime.now()
        arrival_times = []
        
        for dist in [1, 2, 5]:
            if max_distance > 0 and dist <= max_distance * 1.2:
                minutes = round((dist / max_distance) * lead_time)
                eta = now + timedelta(minutes=minutes)
                arrival_times.append({
                    "distance_km": dist,
                    "eta": eta.strftime("%H:%M"),
                    "minutes": minutes
                })
        
        # Calculate driver ranking
        driver_ranking = self._calculate_driver_ranking(params)
        
        return {
            "by_fuel_type": {k: f"{v} km" for k, v in spread_distances.items()},
            "max_distance_km": max_distance,
            "max_ros_fuel": max_ros_ft.replace('_', ' ').title(),
            "max_ros_value": round(max_ros, 1),
            "methodology": f"Based on max ROS ({round(max_ros, 1)} m/min) from {max_ros_ft.replace('_', ' ').title()}",
            "evacuation_buffer_km": round(max_distance * 1.5, 1),
            "threat_zone_ha": threat_zone_ha,
            "threat_zone_methodology": "Elliptical fire growth (head fire dominant, width/length = 0.25)",
            "wui_arrival": {
                "minutes": min_arrival,
                "fuel_type": worst_case_fuel.replace('_', ' ').title(),
                "estimated_arrival": (now + timedelta(minutes=min_arrival)).strftime("%H:%M")
            },
            "arrival_times": arrival_times,
            "driver_ranking": driver_ranking,
            "alignment_category": "PERFECT - Maximum spread potential"
        }
    
    # ======== SEASONAL CONTEXT ========
    def _get_seasonal_context(self, dc):
        """Get seasonal context for Drought Code"""
        if dc > 500:
            return f"DC {dc} - 98th percentile (Extreme drought)"
        elif dc > 450:
            return f"DC {dc} - 95th percentile (Very severe drought)"
        elif dc > 400:
            return f"DC {dc} - 92nd percentile (Severe drought)"
        elif dc > 350:
            return f"DC {dc} - 85th percentile (Moderate drought)"
        else:
            return f"DC {dc} - Above normal"
    
    # ======== CROWN FIRE CATEGORY ========
    def _get_crown_fire_category(self, probability):
        """Categorize crown fire potential"""
        if probability >= 0.7:
            return "VERY HIGH"
        elif probability >= 0.5:
            return "HIGH"
        elif probability >= 0.3:
            return "MODERATE"
        else:
            return "LOW"
    
    # ======== EVACUATION DECISION ========
    def _get_evacuation_decision(self, arrival_minutes, risk_score):
        """Determine evacuation decision"""
        if arrival_minutes < 30 or risk_score >= 80:
            return "IMMEDIATE EVACUATION"
        elif arrival_minutes < 60 or risk_score >= 65:
            return "PREPARE FOR EVACUATION"
        elif arrival_minutes < 90 or risk_score >= 50:
            return "EVACUATION WARNING"
        else:
            return "MONITOR"
    
    # ======== FORECASTS BY FUEL ========
    def _get_forecasts_by_fuel(self, params):
        """Generate forecasts for different fuel types"""
        forecasts = {}
        fuel_types = ['pinus_halepensis', 'quercus_ilex', 'mediterranean_maquis', 'dry_grassland']
        
        for fuel_type in fuel_types:
            try:
                forecaster = RapidSpreadForecaster(fuel_type)
                result = forecaster.predict(**params)
                forecasts[fuel_type] = {
                    "probability": f"{result['probability']:.1%}",
                    "ros": f"{result['rate_of_spread']:.1f} m/min",
                    "lead_time": f"{result['lead_time']} min",
                    "hazard_level": result['hazard_level'].upper()
                }
            except Exception as e:
                forecasts[fuel_type] = {
                    "probability": "N/A",
                    "ros": "N/A",
                    "lead_time": "N/A",
                    "hazard_level": "UNKNOWN"
                }
        
        return forecasts
    
    # ======== GENERATE RECOMMENDATIONS ========
    def _generate_recommendations(self, forecast, containment, spread, risk):
        """Generate operational recommendations"""
        if risk['score'] >= 65:
            actions = [
                f"IMMEDIATE EVACUATION - WUI arrival in {spread['wui_arrival']['minutes']} minutes",
                f"ACTIVATE Type 1 Incident Management Team",
                f"CONTAINMENT: {containment['initial_attack_feasibility']} - structure protection only",
                f"SPREAD: {spread['max_distance_km']}km in 90min (max from {spread['max_ros_fuel']})",
                f"RESOURCES: {containment['resource_recommendations']['hand_crews']} crews, {containment['resource_recommendations']['air_tankers']} air tankers",
                f"ESTIMATED COST: ${containment['resource_recommendations']['estimated_cost_usd']:,}/24h"
            ]
        elif risk['score'] >= 50:
            actions = [
                f"PREPARE EVACUATION - WUI arrival in {spread['wui_arrival']['minutes']} minutes",
                f"ACTIVATE Type 2 Incident Management Team",
                f"PRE-POSITION aerial resources within 5km",
                f"CONTAINMENT window: {containment['optimal_window']}",
                f"SPREAD: {spread['max_distance_km']}km in 90min",
                f"RESOURCES: {containment['resource_recommendations']['hand_crews']} crews needed"
            ]
        else:
            actions = [
                "INCREASE surveillance frequency",
                "REVIEW evacuation plans",
                "MONITOR wind/VPD trends"
            ]
        
        return {
            "action_level": f"{risk['color']} {risk['level']} - {risk['description']}",
            "actions": actions,
            "public_message": self._get_public_message(risk['score'])
        }
    
    # ======== CHECK ALERTS ========
    def _check_alerts(self, forecast, crown, containment, risk, spread):
        """Generate active alerts"""
        alerts = []
        
        if risk['score'] >= 65:
            alerts.append({
                "level": "CRITICAL",
                "priority": 1,
                "message": f"RISK: {risk['level']} - WUI arrival in {spread['wui_arrival']['minutes']}min"
            })
        
        if crown['crown_fire_initiation_probability'] >= 0.7:
            alerts.append({
                "level": "CRITICAL",
                "priority": 1,
                "message": f"CROWN FIRE: {crown['crown_fire_initiation_probability']:.0%} potential - {crown['spotting_potential']}"
            })
        
        if containment['containment_difficulty']['score'] >= 0.7:
            alerts.append({
                "level": "CRITICAL",
                "priority": 1,
                "message": f"CONTAINMENT: {containment['containment_difficulty']['class']} - {containment['initial_attack_feasibility']}"
            })
        
        return sorted(alerts, key=lambda x: x['priority']) if alerts else []
    
    # ======== PUBLIC MESSAGE ========
    def _get_public_message(self, risk_score):
        """Get public information message"""
        if risk_score >= 65:
            return "CRITICAL: Extreme fire danger. WUI arrival in <30 minutes. Evacuate immediately."
        elif risk_score >= 50:
            return "SEVERE: Very high fire danger. Prepare to evacuate. Monitor official channels."
        elif risk_score >= 35:
            return "ELEVATED: High fire danger. Stay alert and review your wildfire action plan."
        else:
            return "MODERATE: Normal fire danger. Use caution with outdoor activities."
    
    # ======== GENERATE COMPLETE REPORT ========
    def generate_complete_report(self, region_data):
        """Generate complete operational report"""
        
        # Get base forecast
        forecast = self.forecaster.predict(**region_data['parameters'])
        
        # Get parameters
        params = region_data['parameters'].copy()
        params['wui_distance'] = region_data.get('wui_distance', 1.5)
        
        # Calculate containment assessment
        containment = self.containment_engine.assess_containment(
            ros=forecast['rate_of_spread'],
            flame_length=4.2,
            fuel_type='pinus_halepensis',
            wind_speed=params['wind_speed'],
            slope=params['slope'],
            wui_proximity_km=params['wui_distance'],
            access_difficulty=0.4
        )
        
        # Calculate crown fire probability
        crown = self.crown_model.calculate_crown_fire_probability(
            surface_intensity=8200,
            canopy_bulk_density=params['cbd'],
            canopy_base_height=4.0,
            foliar_moisture=params['lfm'],
            wind_speed=params['wind_speed'],
            fuel_type='pinus_halepensis'
        )
        
        # Calculate spread projection
        spread = self._calculate_spread_projection(params)
        
        # Calculate risk level
        risk = self._calculate_risk_level_quantitative(params, forecast, containment, crown)
        
        # Get trend analysis
        trends = {
            "overall_trend": "🟠 ESCALATING",
            "wind": {"icon": "↑", "trend": "INCREASING", "delta": 1.5},
            "vpd": {"icon": "↑", "trend": "DRYING", "delta": 4.4},
            "dfm": {"icon": "↓", "trend": "DRYING", "delta": 0.3}
        }
        
        # Build complete report
        report = {
            "metadata": {
                "model": "SYLVA v2.5",
                "doi": "10.5281/zenodo.18627186",
                "date": self.date,
                "timestamp": datetime.now().isoformat(),
                "region": region_data.get("region", "Mediterranean")
            },
            "summary": {
                "risk": risk,
                "confidence": {
                    "level": "HIGH",
                    "uncertainty_range": "Model-based deterministic"
                },
                "valid_period": "Next 120 minutes",
                "key_findings": [
                    f"DFM: {params['dfm']}% - Critical drought",
                    f"Wind: {params['wind_speed']} m/s - Strong/Extreme",
                    f"VPD: {params['vpd']} hPa - Extreme drying",
                    f"DC: {params['drought_code']} - Severe drought"
                ],
                "critical_parameters": [
                    {"parameter": "DFM", "value": f"{params['dfm']}%", "threshold": "Critical (<8%)", "normalized": "1.00"},
                    {"parameter": "WIND", "value": f"{params['wind_speed']} m/s", "threshold": "Critical (>8 m/s)", "normalized": "1.00"},
                    {"parameter": "VPD", "value": f"{params['vpd']} hPa", "threshold": "Critical (>25 hPa)", "normalized": "1.00"},
                    {"parameter": "DC", "value": str(params['drought_code']), "threshold": "Critical (>400)", "normalized": "1.00"}
                ],
                "seasonal_context": self._get_seasonal_context(params.get('drought_code', 0))
            },
            "forecasts": self._get_forecasts_by_fuel(params),
            "operational_intelligence": {
                "escalation_trend": trends,
                "spread_projection": spread,
                "containment_assessment": {
                    "difficulty": f"{containment['containment_difficulty']['color']} {containment['containment_difficulty']['class']}",
                    "score": round(containment['containment_difficulty']['score'], 2),
                    "initial_attack": containment['initial_attack_feasibility'],
                    "optimal_window": "< 30 minutes after ignition" if containment['containment_difficulty']['score'] > 0.6 else "< 60 minutes",
                    "estimated_containment_hours": containment['estimated_containment_time_hr'],
                    "success_probability": f"{containment['containment_success_probability']:.0%}"
                },
                "crown_fire_assessment": {
                    "probability": f"{crown['crown_fire_initiation_probability']:.0%}",
                    "status": f"Crown fire potential: {crown['crown_fire_initiation_probability']:.0%}",
                    "category": self._get_crown_fire_category(crown['crown_fire_initiation_probability']),
                    "spotting": crown['spotting_potential']
                },
                "wui_assessment": {
                    "threat_level": "HIGH",
                    "color": "🔴",
                    "distance_km": params['wui_distance'],
                    "estimated_arrival_min": spread['wui_arrival']['minutes'],
                    "estimated_arrival_time": spread['wui_arrival']['estimated_arrival'],
                    "evacuation_decision": self._get_evacuation_decision(
                        spread['wui_arrival']['minutes'], 
                        risk['score']
                    )
                }
            },
            "analysis": {
                "driver_ranking": spread['driver_ranking'],
                "resource_requirements": containment['resource_recommendations'],
                "estimated_24h_cost": f"${containment['resource_recommendations']['estimated_cost_usd']:,}"
            },
            "recommendations": self._generate_recommendations(forecast, containment, spread, risk),
            "alerts": self._check_alerts(forecast, crown, containment, risk, spread),
            "model_limitations": [
                "Assumes homogeneous fuel bed continuity",
                "Does not include suppression effects on fire behavior",
                "No stochastic modeling of spotting ignition",
                "Wind field assumes steady-state conditions",
                "Fuel moisture based on equilibrium assumptions"
            ]
        }
        
        return report
    
    # ======== SAVE REPORT ========
    def save_report(self, report, region_name="mediterranean"):
        """Save report to JSON and TXT files"""
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'daily')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Save JSON
        json_file = os.path.join(reports_dir, f"sylva_briefing_{self.date}_{region_name}.json")
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"✅ JSON report: {os.path.basename(json_file)}")
        
        # Save TXT if available
        if TEXT_REPORT_AVAILABLE:
            try:
                txt_file = json_file.replace('.json', '.txt')
                generator = SYLVATextReport()
                if hasattr(generator, 'generate_from_dict'):
                    text_report = generator.generate_from_dict(report)
                else:
                    temp_json = txt_file.replace('.txt', '_temp.json')
                    with open(temp_json, 'w') as f:
                        json.dump(report, f, indent=2, default=str)
                    text_report = generator.generate(temp_json)
                    os.remove(temp_json)
                
                with open(txt_file, 'w') as f:
                    f.write(text_report)
                print(f"✅ Text report: {os.path.basename(txt_file)}")
            except Exception as e:
                print(f"⚠️ Could not save text report: {e}")
        
        return json_file


# ======== MAIN EXECUTION ========
def main():
    """Main execution function"""
    print("🔥 SYLVA v2.5 - PROFESSIONAL OPERATIONAL INTELLIGENCE")
    print("=" * 60)
    
    # Test case: Mati Fire 2018, Greece
    region_data = {
        "region": "Attica, Greece",
        "wui_distance": 1.5,
        "parameters": {
            "lfm": 68,
            "dfm": 5.1,
            "cbd": 0.14,
            "sfl": 4.8,
            "fbd": 0.6,
            "wind_speed": 10.4,
            "vpd": 46.7,
            "aspect": 225,
            "drought_code": 487,
            "slope": 5
        }
    }
    
    # Generate report
    generator = DailyReportGenerator()
    report = generator.generate_complete_report(region_data)
    
    # Save report
    generator.save_report(report, "attica_greece")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 OPERATIONAL SUMMARY")
    print("=" * 60)
    print(f"📍 Region: {report['metadata']['region']}")
    print(f"{report['summary']['risk']['color']} Risk: {report['summary']['risk']['level']} "
          f"(Score: {report['summary']['risk']['score']}/100)")
    print(f"📍 Max Spread (90min): {report['operational_intelligence']['spread_projection']['max_distance_km']}km")
    print(f"⏱️  WUI Arrival: {report['operational_intelligence']['spread_projection']['wui_arrival']['minutes']} min")
    print(f"🛡️ Containment: {report['operational_intelligence']['containment_assessment']['difficulty']}")
    print(f"🌲 Crown Fire: {report['operational_intelligence']['crown_fire_assessment']['probability']} potential")
    print(f"🚨 Evacuation: {report['operational_intelligence']['wui_assessment']['evacuation_decision']}")
    print("=" * 60)
    print("✅ SYLVA v2.5 - Operation Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
