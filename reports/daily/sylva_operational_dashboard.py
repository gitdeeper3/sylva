#!/usr/bin/env python3
"""SYLVA Operational Dashboard - Command Center Ready - FIXED FORMATTING"""

import json
from datetime import datetime

class OperationalDashboard:
    """Generate command-center ready operational briefings"""
    
    def __init__(self):
        self.separator = "=" * 80
        self.divider = "─" * 80
        self.light_divider = "·" * 80
        
    def generate_from_json(self, json_file):
        """Generate operational dashboard from JSON report"""
        with open(json_file, 'r') as f:
            data = json.load(f)
        return self._format_dashboard(data)
    
    def _format_dashboard(self, data):
        """Format report as command-center dashboard"""
        lines = []
        
        # ============ HEADER ============
        risk = data['summary']['risk']
        lines.append(self.separator)
        lines.append(f"🔥 SYLVA OPERATIONAL DASHBOARD {risk['color']} {risk['level']} RISK")
        lines.append(self.separator)
        lines.append(f"📍 {data['metadata']['region']}          ⏱️  {data['metadata']['timestamp'][:19]}          🔗 DOI: {data['metadata']['doi']}")
        lines.append("")
        
        # ============ EXECUTIVE SUMMARY ============
        lines.append("📊 EXECUTIVE SUMMARY")
        lines.append(self.divider)
        lines.append(f"RISK LEVEL:     {risk['color']} {risk['level']} (Score: {risk['score']}/100)")
        lines.append(f"DESCRIPTION:    {risk['description']}")
        lines.append(f"CONFIDENCE:     {data['summary']['confidence']['level']}")
        lines.append(f"VALID PERIOD:   {data['summary']['valid_period']}")
        lines.append("")
        
        # Key Findings - Visual Format
        lines.append("⚠️  CRITICAL FINDINGS:")
        for finding in data['summary']['key_findings'][:4]:
            lines.append(f"  • {finding}")
        lines.append("")
        
        # ============ FIRE ENVIRONMENT TREND ============
        # FIXED: Convert dict to readable text format
        lines.append("🔥 FIRE ENVIRONMENT TREND")
        lines.append(self.divider)
        
        trend = data['operational_intelligence']['escalation_trend']
        
        # Overall trend with color
        overall = trend['overall_trend']
        if 'ESCALATING RAPIDLY' in overall:
            overall_display = f"🔴 {overall}"
        elif 'ESCALATING' in overall:
            overall_display = f"🟠 {overall}"
        elif 'STABLE' in overall:
            overall_display = f"🟡 {overall}"
        else:
            overall_display = f"🟢 {overall}"
            
        lines.append(f"OVERALL:    {overall_display}")
        lines.append("")
        
        # Wind trend - FIXED: Readable format
        wind = trend['wind']
        wind_icon = wind['icon']
        wind_trend = wind['trend']
        wind_delta = wind['delta']
        lines.append(f"WIND:       {wind_icon} {wind_trend} (Δ{wind_delta:+0.1f} m/s)")
        
        # VPD trend - FIXED: Readable format
        vpd = trend['vpd']
        vpd_icon = vpd['icon']
        vpd_trend = vpd['trend']
        vpd_delta = vpd['delta']
        lines.append(f"VPD:        {vpd_icon} {vpd_trend} (Δ{vpd_delta:+0.1f} hPa)")
        
        # DFM trend - FIXED: Readable format
        dfm = trend['dfm']
        dfm_icon = dfm['icon']
        dfm_trend = dfm['trend']
        dfm_delta = dfm['delta']
        lines.append(f"DFM:        {dfm_icon} {dfm_trend} (Δ{dfm_delta:+0.1f}%)")
        lines.append("")
        
        # ============ FIRE BEHAVIOR MATRIX ============
        lines.append("📈 FIRE BEHAVIOR FORECAST")
        lines.append(self.divider)
        lines.append("")
        lines.append("FUEL TYPE           ROS (m/min)    PROBABILITY    LEAD TIME    HAZARD")
        lines.append("────────────────────────────────────────────────────────────────")
        
        forecasts = data['forecasts']
        for fuel, fc in forecasts.items():
            if 'probability' in fc and 'N/A' not in fc['probability']:
                name = fuel.replace('_', ' ').title()[:18].ljust(18)
                ros = fc['ros'].replace(' m/min', '').rjust(8)
                prob = fc['probability'].rjust(8)
                lead = fc['lead_time'].rjust(8)
                hazard = fc['hazard_level'].rjust(10)
                
                # Color code hazard level
                if 'IMMINENT' in hazard:
                    hazard = f"🔴{hazard[4:]}"
                elif 'WARNING' in hazard:
                    hazard = f"🟠{hazard[4:]}"
                elif 'WATCH' in hazard:
                    hazard = f"🟡{hazard[4:]}"
                
                lines.append(f"{name} {ros} m/min    {prob}    {lead}    {hazard}")
        lines.append("")
        
        # ============ SPREAD PROJECTION ============
        spread = data['operational_intelligence']['spread_projection']
        lines.append("📍 SPREAD PROJECTION")
        lines.append(self.divider)
        lines.append(f"MAXIMUM SPREAD:     {spread['max_distance_km']} km in 90 minutes")
        lines.append(f"DRIVER FUEL TYPE:   {spread['max_ros_fuel']} ({spread['max_ros_value']} m/min)")
        lines.append(f"THREAT ZONE:        {spread['threat_zone_ha']} ha (Elliptical model)")
        lines.append(f"EVACUATION BUFFER:  {spread['evacuation_buffer_km']} km")
        lines.append("")
        
        # WUI Threat
        wui = spread['wui_arrival']
        lines.append(f"🏠 WUI THREAT:       {wui['fuel_type']} - Arrival in {wui['minutes']} minutes")
        lines.append(f"                     Estimated: {wui['estimated_arrival']}")
        lines.append("")
        
        # Arrival Times
        lines.append("⏱️  ETA TO KEY DISTANCES:")
        for eta in spread['arrival_times']:
            lines.append(f"   {eta['distance_km']} km: {eta['eta']} ({eta['minutes']} min)")
        lines.append("")
        
        # ============ CONTAINMENT & CROWN FIRE ============
        containment = data['operational_intelligence']['containment_assessment']
        crown = data['operational_intelligence']['crown_fire_assessment']
        
        lines.append("🛡️  CONTAINMENT ASSESSMENT")
        lines.append(self.divider)
        lines.append(f"DIFFICULTY:         {containment['difficulty']}")
        lines.append(f"INITIAL ATTACK:     {containment['initial_attack']}")
        lines.append(f"OPTIMAL WINDOW:     {containment['optimal_window']}")
        lines.append(f"SUCCESS PROB:       {containment['success_probability']}")
        lines.append("")
        
        # Crown Fire - Color Coded
        crown_category = crown['category']
        crown_color = "🔴" if "VERY HIGH" in crown_category else "🟠" if "HIGH" in crown_category else "🟡"
        
        lines.append("🌲 CROWN FIRE POTENTIAL")
        lines.append(self.divider)
        lines.append(f"PROBABILITY:        {crown_color} {crown['probability']} - {crown['category']}")
        lines.append(f"SPOTTING:           {crown['spotting']}")
        lines.append("")
        
        # ============ WUI DECISION ============
        wui_decision = data['operational_intelligence']['wui_assessment']
        lines.append("🚨 EVACUATION DECISION")
        lines.append(self.divider)
        
        # Color code evacuation decision
        decision = wui_decision['evacuation_decision']
        if 'IMMEDIATE' in decision:
            decision = f"🔴 {decision}"
        elif 'PREPARE' in decision:
            decision = f"🟠 {decision}"
        elif 'WARNING' in decision:
            decision = f"🟡 {decision}"
        else:
            decision = f"🟢 {decision}"
            
        lines.append(f"COMMAND DECISION:   {decision}")
        lines.append(f"WUI DISTANCE:       {wui_decision['distance_km']} km")
        lines.append(f"ESTIMATED ARRIVAL:  {wui_decision['estimated_arrival_min']} minutes")
        lines.append("")
        
        # ============ RISK DRIVERS ============
        drivers = data['analysis']['driver_ranking']
        lines.append("🎯 PRIMARY RISK DRIVERS")
        lines.append(self.divider)
        
        # Display top 3 drivers with visual bars
        driver_items = list(drivers.items())[:3]
        for i, (driver, value) in enumerate(driver_items, 1):
            percent = int(value.replace('%', ''))
            bar = "█" * (percent // 10)
            lines.append(f"{i}. {driver}: {value} {bar}")
        lines.append("")
        
        # ============ RESOURCE REQUIREMENTS ============
        resources = data['analysis']['resource_requirements']
        lines.append("🚒 RESOURCE REQUIREMENTS")
        lines.append(self.divider)
        lines.append(f"HAND CREWS:     {resources['hand_crews']}")
        lines.append(f"FIRE ENGINES:   {resources['fire_engines']}")
        lines.append(f"AIR TANKERS:    {resources['air_tankers']}")
        lines.append(f"HELICOPTERS:    {resources['helicopters']}")
        lines.append(f"DOZERS:         {resources['dozers']}")
        lines.append(f"OVERHEAD:       {resources['overhead']}")
        lines.append(f"24h COST:       {data['analysis']['estimated_24h_cost']}")
        lines.append("")
        
        # ============ SEASONAL CONTEXT ============
        lines.append("📅 SEASONAL CONTEXT")
        lines.append(self.divider)
        lines.append(f"{data['summary']['seasonal_context']}")
        lines.append("")
        
        # ============ OPERATIONAL DIRECTIVES ============
        lines.append("⚡ OPERATIONAL DIRECTIVES")
        lines.append(self.divider)
        
        rec = data['recommendations']
        lines.append(f"ACTION LEVEL:   {rec['action_level']}")
        lines.append("")
        lines.append("IMMEDIATE ACTIONS:")
        for i, action in enumerate(rec['actions'][:5], 1):
            lines.append(f"  {i}. {action}")
        lines.append("")
        lines.append(f"PUBLIC INFO:    {rec['public_message']}")
        lines.append("")
        
        # ============ ACTIVE ALERTS ============
        alerts = data['alerts']
        if alerts:
            lines.append("🔴 ACTIVE ALERTS")
            lines.append(self.divider)
            for alert in alerts[:3]:
                alert_level = alert['level']
                if 'CRITICAL' in alert_level:
                    alert_level = f"🔴 {alert_level}"
                elif 'SEVERE' in alert_level:
                    alert_level = f"🟠 {alert_level}"
                elif 'HIGH' in alert_level:
                    alert_level = f"🟡 {alert_level}"
                lines.append(f"  • {alert_level}: {alert['message']}")
            lines.append("")
        
        # ============ MODEL LIMITATIONS ============
        lines.append("⚠️  MODEL LIMITATIONS")
        lines.append(self.divider)
        for limitation in data['model_limitations'][:3]:
            lines.append(f"  • {limitation}")
        lines.append("")
        
        # ============ FOOTER ============
        lines.append(self.separator)
        lines.append(f"✅ SYLVA v2.5 Operational Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("🔗 DOI: 10.5281/zenodo.18627186 | Command Center Authorized Use Only")
        lines.append(self.separator)
        
        return '\n'.join(lines)


def main():
    """Generate operational dashboard from latest report"""
    import os
    from pathlib import Path
    
    reports_dir = Path("reports/daily")
    json_files = list(reports_dir.glob("sylva_briefing_*.json"))
    
    if not json_files:
        print("❌ No JSON reports found")
        return
    
    # Get latest report
    latest = max(json_files, key=lambda f: f.stat().st_mtime)
    print(f"📊 Generating Operational Dashboard from: {latest.name}")
    
    # Generate dashboard
    dashboard = OperationalDashboard()
    output = dashboard.generate_from_json(str(latest))
    
    # Save dashboard
    dashboard_file = latest.with_name(latest.name.replace('.json', '_DASHBOARD.txt'))
    with open(dashboard_file, 'w') as f:
        f.write(output)
    
    print(f"✅ Operational Dashboard saved: {dashboard_file.name}")
    print("\n" + "=" * 80)
    print("📋 DASHBOARD PREVIEW")
    print("=" * 80)
    print("\n".join(output.split('\n')[:25]) + "\n...")


if __name__ == "__main__":
    main()
