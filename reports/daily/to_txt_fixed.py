#!/usr/bin/env python3
"""SYLVA Professional Text Report Generator - FIXED"""

import json
import sys
import textwrap
from datetime import datetime
from pathlib import Path

class SYLVATextReport:
    """Professional text report generator for SYLVA"""
    
    def __init__(self, width=90):
        self.width = width
        self.separator = "=" * self.width
        self.divider = "-" * self.width
        self.light_divider = "·" * self.width
    
    def generate(self, json_file):
        """Generate from JSON file"""
        with open(json_file, 'r') as f:
            data = json.load(f)
        return self.generate_from_dict(data)
    
    def generate_from_dict(self, data):
        """Generate formatted text report from dictionary"""
        lines = []
        
        # ============ HEADER ============
        lines.append(self.separator)
        lines.append("🔥 SYLVA RAPID FIRE SPREAD FORECAST - OPERATIONAL BRIEFING".center(self.width))
        lines.append(self.separator)
        lines.append("")
        
        # ============ METADATA ============
        metadata = data.get('metadata', {})
        lines.append(f"DATE:          {metadata.get('date', 'Unknown')}")
        lines.append(f"TIME:          {metadata.get('timestamp', 'Unknown')[:19]}")
        lines.append(f"REGION:        {metadata.get('region', 'Unknown')}")
        lines.append(f"MODEL:         {metadata.get('model', 'SYLVA v2.2')}")
        lines.append(f"DOI:           {metadata.get('doi', '10.5281/zenodo.18627186')}")
        lines.append("")
        lines.append(self.divider)
        lines.append("")
        
        # ============ EXECUTIVE SUMMARY ============
        summary = data.get('summary', {})
        risk = summary.get('risk', {})
        confidence = summary.get('confidence', {})
        
        lines.append("📊 EXECUTIVE SUMMARY")
        lines.append(self.light_divider)
        lines.append("")
        lines.append(f"Risk Level:     {risk.get('color', '')} {risk.get('level', 'N/A')} (Score: {risk.get('score', 0)}/100)")
        lines.append(f"Description:    {risk.get('description', 'N/A')}")
        lines.append(f"Confidence:     {confidence.get('level', 'N/A')} ({confidence.get('uncertainty_range', 'N/A')})")
        lines.append(f"Valid Period:   {summary.get('valid_period', 'Next 120 minutes')}")
        lines.append("")
        
        # Key Findings
        lines.append("KEY FINDINGS:")
        for finding in summary.get('key_findings', []):
            lines.append(f"  • {finding}")
        lines.append("")
        
        # Critical Parameters
        lines.append("CRITICAL PARAMETERS:")
        for param in summary.get('critical_parameters', []):
            lines.append(f"  • {param.get('parameter', 'N/A')}: {param.get('value', 'N/A')} ({param.get('threshold', 'N/A')}) [Norm: {param.get('normalized', 'N/A')}]")
        lines.append("")
        lines.append(self.divider)
        lines.append("")
        
        # ============ FORECAST SUMMARY ============
        lines.append("📈 FORECAST SUMMARY")
        lines.append(self.light_divider)
        lines.append("")
        
        forecasts = data.get('forecasts', {})
        for fuel_type, forecast in forecasts.items():
            if isinstance(forecast, dict):
                fuel_name = fuel_type.replace('_', ' ').title()
                lines.append(fuel_name)
                lines.append(f"  Probability:  {forecast.get('probability', 'N/A')}")
                lines.append(f"  ROS:          {forecast.get('ros', 'N/A')}")
                lines.append(f"  Lead Time:    {forecast.get('lead_time', 'N/A')}")
                lines.append("")
        
        lines.append(self.divider)
        lines.append("")
        
        # ============ OPERATIONAL INTELLIGENCE ============
        ops = data.get('operational_intelligence', {})
        
        # Escalation Trend
        trend = ops.get('escalation_trend', {})
        lines.append("🔥 FIRE ENVIRONMENT TREND")
        lines.append(self.light_divider)
        lines.append("")
        lines.append(f"Overall: {trend.get('overall', 'N/A')}")
        lines.append(f"Wind:    {trend.get('wind', 'N/A')}")
        lines.append(f"VPD:     {trend.get('vpd', 'N/A')}")
        lines.append(f"DFM:     {trend.get('dfm', 'N/A')}")
        lines.append("")
        lines.append(self.divider)
        lines.append("")
        
        # Spread Projection
        spread = ops.get('spread_projection', {})
        lines.append("📍 SPREAD PROJECTION")
        lines.append(self.light_divider)
        lines.append("")
        lines.append(f"Distance (90min): {spread.get('distance_km', 'N/A')} km")
        lines.append(f"Methodology:      {spread.get('methodology', 'N/A')}")
        lines.append(f"Evacuation Buffer: {spread.get('evacuation_buffer_km', 'N/A')} km")
        lines.append(f"Threat Zone:      {spread.get('threat_zone_ha', 'N/A')} ha")
        lines.append("")
        lines.append("ETA to Key Distances:")
        for eta in spread.get('arrival_times', [])[:3]:
            lines.append(f"  • {eta.get('distance_km', 0)} km: {eta.get('eta', 'N/A')} ({eta.get('minutes', 0)} min)")
        lines.append("")
        lines.append(self.divider)
        lines.append("")
        
        # Containment
        containment = ops.get('containment_assessment', {})
        lines.append("🛡️ CONTAINMENT DIFFICULTY")
        lines.append(self.light_divider)
        lines.append("")
        lines.append(f"Difficulty: {containment.get('difficulty', 'N/A')}")
        lines.append(f"Score:      {containment.get('score', 0)}/1.0")
        lines.append(f"Initial Attack: {containment.get('initial_attack', 'N/A')}")
        lines.append(f"Optimal Window: {containment.get('optimal_window', 'N/A')}")
        lines.append(f"Est. Containment: {containment.get('estimated_containment_hours', 0)} hours")
        lines.append(f"Success Prob:    {containment.get('success_probability', 'N/A')}")
        lines.append("")
        lines.append(self.divider)
        lines.append("")
        
        # Crown Fire
        crown = ops.get('crown_fire_assessment', {})
        lines.append("🌲 CROWN FIRE POTENTIAL")
        lines.append(self.light_divider)
        lines.append("")
        lines.append(f"Probability: {crown.get('probability', 'N/A')}")
        lines.append(f"Status:      {crown.get('status', 'N/A')}")
        lines.append(f"Category:    {crown.get('category', 'N/A')}")
        lines.append(f"Spotting:    {crown.get('spotting', 'N/A')}")
        lines.append("")
        lines.append(self.divider)
        lines.append("")
        
        # WUI Threat
        wui = ops.get('wui_assessment', {})
        lines.append("🏠 WUI THREAT ASSESSMENT")
        lines.append(self.light_divider)
        lines.append("")
        lines.append(f"Threat Level: {wui.get('color', '')} {wui.get('threat_level', 'N/A')}")
        lines.append(f"Distance:     {wui.get('distance_km', 0)} km")
        lines.append(f"Arrival:      {wui.get('estimated_arrival_min', 0)} minutes")
        lines.append(f"Structures:   {wui.get('structure_threat_count', 'N/A')}")
        lines.append(f"Decision:     {wui.get('evacuation_decision', 'N/A')}")
        lines.append("")
        lines.append(self.divider)
        lines.append("")
        
        # ============ ANALYSIS ============
        analysis = data.get('analysis', {})
        lines.append("📊 RISK ANALYSIS")
        lines.append(self.light_divider)
        lines.append("")
        lines.append(f"Primary Drivers: {', '.join(list(analysis.get('driver_ranking', {}).keys())[:3])}")
        lines.append(f"Resource Cost:   {analysis.get('estimated_24h_cost', 'N/A')}/24h")
        lines.append("")
        lines.append("Resource Requirements:")
        resources = analysis.get('resource_requirements', {})
        lines.append(f"  • Hand Crews:  {resources.get('hand_crews', 0)}")
        lines.append(f"  • Fire Engines: {resources.get('fire_engines', 0)}")
        lines.append(f"  • Air Tankers: {resources.get('air_tankers', 0)}")
        lines.append(f"  • Helicopters: {resources.get('helicopters', 0)}")
        lines.append(f"  • Dozers:      {resources.get('dozers', 0)}")
        lines.append(f"  • Overhead:    {resources.get('overhead', 'N/A')}")
        lines.append("")
        lines.append(self.divider)
        lines.append("")
        
        # ============ RECOMMENDATIONS ============
        rec = data.get('recommendations', {})
        lines.append("🚨 OPERATIONAL RECOMMENDATIONS")
        lines.append(self.light_divider)
        lines.append("")
        lines.append(f"{rec.get('action_level', 'N/A')}")
        lines.append("")
        lines.append("ACTIONS:")
        for action in rec.get('actions', [])[:5]:
            lines.append(f"  • {action}")
        lines.append("")
        lines.append(f"PUBLIC MESSAGE: {rec.get('public_message', 'N/A')}")
        lines.append("")
        lines.append(self.divider)
        lines.append("")
        
        # ============ SEASONAL CONTEXT ============
        lines.append("📅 SEASONAL CONTEXT")
        lines.append(self.light_divider)
        lines.append("")
        lines.append(f"{summary.get('seasonal_context', 'N/A')}")
        lines.append("")
        lines.append(self.divider)
        lines.append("")
        
        # ============ FOOTER ============
        lines.append("📌 REPORT INFORMATION")
        lines.append(self.light_divider)
        lines.append("")
        lines.append(f"Generated:  {metadata.get('timestamp', 'Unknown')}")
        lines.append(f"Model:      {metadata.get('model', 'SYLVA v2.2')}")
        lines.append(f"DOI:        {metadata.get('doi', '10.5281/zenodo.18627186')}")
        lines.append("")
        lines.append("⚠️  DISCLAIMER")
        lines.append("  This is an automated decision support tool. Always use professional")
        lines.append("  judgment and consider multiple information sources. Not a substitute")
        lines.append("  for operational expertise and local knowledge.")
        lines.append("")
        lines.append(self.separator)
        
        return '\n'.join(lines)
