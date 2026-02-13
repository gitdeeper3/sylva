#!/usr/bin/env python3
"""Convert SYLVA daily report to plain text format"""

import json
import sys
from datetime import datetime
from pathlib import Path

def json_to_txt(json_file):
    """Convert JSON report to plain text file"""
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return
    
    print(f"📄 Processing: {json_file}")
    
    # Create output filename
    txt_file = json_file.replace('.json', '.txt')
    
    # Extract metadata
    metadata = data.get('metadata', {})
    summary = data.get('summary', {})
    parameters = data.get('parameters', {})
    forecasts = data.get('forecasts', {})
    recommendations = data.get('recommendations', {})
    alerts = data.get('alerts', {})
    
    # Build text content
    lines = []
    
    # Header
    lines.append("=" * 80)
    lines.append("🔥 SYLVA RAPID FIRE SPREAD FORECAST - DAILY BRIEFING")
    lines.append("=" * 80)
    lines.append("")
    
    # Metadata
    lines.append(f"DATE:          {metadata.get('date', 'Unknown')}")
    lines.append(f"TIME:          {metadata.get('timestamp', 'Unknown')[:19]}")
    lines.append(f"REGION:        {metadata.get('region', 'Unknown')}")
    lines.append(f"MODEL:         {metadata.get('model', 'SYLVA v2.5.0')}")
    lines.append(f"DOI:           {metadata.get('doi', '10.5281/zenodo.18627186')}")
    lines.append("")
    lines.append("-" * 80)
    lines.append("")
    
    # Executive Summary
    lines.append("📊 EXECUTIVE SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Risk Level:     {summary.get('risk_level', 'N/A')}")
    lines.append(f"Confidence:     {summary.get('confidence', 'N/A')}")
    lines.append(f"Valid Period:   {summary.get('valid_period', 'Next 120 minutes')}")
    lines.append("")
    
    # Key Findings
    lines.append("🔍 KEY FINDINGS:")
    for finding in summary.get('key_findings', []):
        lines.append(f"  • {finding}")
    lines.append("")
    
    # Critical Parameters
    lines.append("⚠️ CRITICAL PARAMETERS:")
    for param in summary.get('critical_parameters', []):
        lines.append(f"  • {param.get('parameter', 'N/A')}: {param.get('normalized_value', 'N/A')} ({param.get('threshold', 'N/A')})")
    lines.append("")
    lines.append("-" * 80)
    lines.append("")
    
    # Forecast Summary
    lines.append("📈 FORECAST SUMMARY")
    lines.append("-" * 40)
    
    if forecasts:
        for fuel_type, forecast in forecasts.items():
            if isinstance(forecast, dict) and 'probability' in forecast:
                fuel_name = fuel_type.replace('_', ' ').title()
                lines.append(f"\n{fuel_name}:")
                lines.append(f"  • Probability:  {forecast.get('probability', 0):.1%}")
                lines.append(f"  • Hazard Level: {forecast.get('hazard_level', 'unknown').upper()}")
                lines.append(f"  • Lead Time:    {forecast.get('lead_time', 0)} minutes")
                lines.append(f"  • ROS:          {forecast.get('ros', 0):.1f} m/min")
                lines.append(f"  • RSI:          {forecast.get('rsi', 0):.3f}")
    else:
        lines.append("  No forecast data available")
    lines.append("")
    lines.append("-" * 80)
    lines.append("")
    
    # Input Parameters
    lines.append("📋 INPUT PARAMETERS")
    lines.append("-" * 40)
    
    raw_params = parameters.get('raw', {})
    if raw_params:
        for key, value in raw_params.items():
            lines.append(f"  {key.upper():12s}: {value}")
    else:
        lines.append("  No parameter data available")
    lines.append("")
    
    # Normalized Parameters
    norm_params = parameters.get('normalized', {})
    if norm_params:
        lines.append("  Normalized Values (0-1):")
        for key, value in norm_params.items():
            lines.append(f"    {key:12s}: {value:.3f}")
    lines.append("")
    lines.append("-" * 80)
    lines.append("")
    
    # Operational Recommendations
    lines.append("🚨 OPERATIONAL RECOMMENDATIONS")
    lines.append("-" * 40)
    lines.append(f"Action Level: {recommendations.get('action_level', 'N/A')}")
    lines.append("")
    
    lines.append("Actions Required:")
    for action in recommendations.get('actions', []):
        lines.append(f"  • {action}")
    lines.append("")
    
    # Resources
    resources = recommendations.get('resources', {})
    if resources:
        lines.append("Resource Recommendations:")
        for key, value in resources.items():
            lines.append(f"  • {key.title()}: {value}")
    lines.append("")
    
    # Public Message
    lines.append("Public Message:")
    lines.append(f"  {recommendations.get('public_message', 'No message')}")
    lines.append("")
    lines.append("-" * 80)
    lines.append("")
    
    # Active Alerts
    lines.append("🔴 ACTIVE ALERTS")
    lines.append("-" * 40)
    
    active_alerts = alerts.get('active_alerts', [])
    if active_alerts:
        lines.append(f"Total Alerts: {alerts.get('total_alerts', 0)}")
        lines.append(f"Highest Level: {alerts.get('highest_level', 'NONE')}")
        lines.append("")
        for alert in active_alerts:
            lines.append(f"  • [{alert.get('level', 'ALERT')}] {alert.get('message', 'No message')}")
            lines.append(f"    Lead time: {alert.get('lead_time', 0)} minutes")
    else:
        lines.append("  No active alerts")
    lines.append("")
    lines.append("-" * 80)
    lines.append("")
    
    # Parameter Definitions
    lines.append("📚 PARAMETER DEFINITIONS")
    lines.append("-" * 40)
    
    definitions = data.get('appendix', {}).get('parameter_definitions', {})
    if definitions:
        for key, value in definitions.items():
            lines.append(f"  {key}: {value}")
    else:
        lines.append("  • LFM: Live Fuel Moisture - moisture content in living vegetation")
        lines.append("  • DFM: Dead Fuel Moisture - moisture content in dead fuels")
        lines.append("  • CBD: Canopy Bulk Density - mass of available crown fuel")
        lines.append("  • SFL: Surface Fuel Load - combustible material per unit area")
        lines.append("  • FBD: Fuel Bed Depth - vertical thickness of surface fuel")
        lines.append("  • Vw: Wind Vector - terrain-adjusted wind speed")
        lines.append("  • VPD: Vapor Pressure Deficit - atmospheric drying power")
        lines.append("  • Aspect: Slope orientation relative to solar radiation")
        lines.append("  • DC: Drought Code - seasonal drought effects")
    lines.append("")
    lines.append("-" * 80)
    lines.append("")
    
    # Footer
    lines.append("📌 REPORT INFORMATION")
    lines.append("-" * 40)
    lines.append(f"Generated: {metadata.get('timestamp', 'Unknown')}")
    lines.append(f"Model Version: {metadata.get('model', 'SYLVA v2.5.0')}")
    lines.append(f"DOI: {metadata.get('doi', '10.5281/zenodo.18627186')}")
    lines.append("")
    lines.append("⚠️  DISCLAIMER: This is an automated decision support tool.")
    lines.append("   Always use professional judgment and consider multiple information sources.")
    lines.append("   Not a substitute for operational expertise and local knowledge.")
    lines.append("")
    lines.append("=" * 80)
    
    # Write to file
    try:
        with open(txt_file, 'w') as f:
            f.write('\n'.join(lines))
        print(f"✅ Text report generated: {txt_file}")
        
        # Also print to console for quick view
        print("\n" + "=" * 60)
        print("📋 PREVIEW (first 20 lines):")
        print("=" * 60)
        for line in lines[:20]:
            print(line)
        print("..." + "\n")
        
    except Exception as e:
        print(f"❌ Error saving text file: {e}")


def process_latest_report():
    """Process the most recent JSON report"""
    reports_dir = Path("reports/daily")
    if not reports_dir.exists():
        print("❌ reports/daily/ directory not found")
        return
    
    json_files = list(reports_dir.glob("*.json"))
    # Exclude template file
    json_files = [f for f in json_files if 'template' not in f.name]
    
    if not json_files:
        print("❌ No JSON reports found")
        return
    
    # Get the most recent file
    latest = max(json_files, key=lambda f: f.stat().st_mtime)
    print(f"📂 Latest report: {latest.name}")
    json_to_txt(str(latest))


def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Process specific file
        json_to_txt(sys.argv[1])
    else:
        # Process latest report
        process_latest_report()


if __name__ == "__main__":
    main()
