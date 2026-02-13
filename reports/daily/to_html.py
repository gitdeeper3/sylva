#!/usr/bin/env python3
"""Convert SYLVA daily report to HTML"""

import json
import sys
from pathlib import Path

def json_to_html(json_file):
    """Convert JSON report to HTML dashboard"""
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return
    
    # Check if forecasts exist
    if 'forecasts' not in data:
        print("❌ No forecasts data in report")
        return
    
    # Get lead time safely
    lead_time = "N/A"
    forecasts = data.get('forecasts', {})
    if forecasts:
        first_forecast = next(iter(forecasts.values()))
        lead_time = first_forecast.get('lead_time', 'N/A')
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SYLVA Daily Briefing - {data.get('metadata', {}).get('date', 'Unknown')}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            background: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .risk-EXTREME {{ background: #c0392b; }}
        .risk-HIGH {{ background: #e67e22; }}
        .risk-MODERATE {{ background: #f39c12; }}
        .risk-LOW {{ background: #27ae60; }}
        .risk-NORMAL {{ background: #2980b9; }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .card h3 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        .metric {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .alert {{
            background: #fdeaea;
            border-left: 4px solid #c0392b;
            padding: 15px;
            margin-bottom: 10px;
        }}
        .warning {{
            background: #fff3e0;
            border-left: 4px solid #e67e22;
        }}
        .success {{
            background: #e8f5e9;
            border-left: 4px solid #27ae60;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            color: white;
            font-size: 12px;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header risk-{data.get('summary', {}).get('risk_level', 'NORMAL')}">
            <h1>🔥 SYLVA Rapid Fire Spread Briefing</h1>
            <p><strong>Date:</strong> {data.get('metadata', {}).get('date', 'Unknown')}</p>
            <p><strong>Region:</strong> {data.get('metadata', {}).get('region', 'Unknown')}</p>
            <p><strong>Valid Period:</strong> {data.get('summary', {}).get('valid_period', 'Next 120 minutes')}</p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>Risk Assessment</h3>
                <p><span class="metric">{data.get('summary', {}).get('risk_level', 'N/A')}</span></p>
                <p>Confidence: {data.get('summary', {}).get('confidence', 'N/A')}</p>
                <p>Lead Time: {lead_time} min</p>
            </div>
            <div class="card">
                <h3>Critical Parameters</h3>
                <ul>
"""
    
    # Add critical parameters
    critical_params = data.get('summary', {}).get('critical_parameters', [])
    for param in critical_params:
        html += f"                    <li><strong>{param.get('parameter', 'N/A')}:</strong> {param.get('normalized_value', 'N/A')} ({param.get('threshold', 'N/A')})</li>\n"
    
    html += """                </ul>
            </div>
            <div class="card">
                <h3>Active Alerts</h3>
                <p><span class="metric">{}</span></p>
                <p>Highest Level: {}</p>
            </div>
        </div>
        
        <h2>📊 Forecast by Fuel Type</h2>
        <table>
            <thead>
                <tr>
                    <th>Fuel Type</th>
                    <th>Probability</th>
                    <th>Hazard Level</th>
                    <th>ROS (m/min)</th>
                    <th>Lead Time</th>
                </tr>
            </thead>
            <tbody>
""".format(
    len(data.get('alerts', {}).get('active_alerts', [])),
    data.get('alerts', {}).get('highest_level', 'NONE')
)
    
    # Add forecasts
    for fuel, forecast in data.get('forecasts', {}).items():
        if isinstance(forecast, dict) and 'probability' in forecast:
            hazard_color = '#c0392b' if forecast.get('hazard_level') == 'imminent' else '#e67e22'
            html += f"""                <tr>
                    <td>{fuel.replace('_', ' ').title()}</td>
                    <td><strong>{forecast.get('probability', 0):.1%}</strong></td>
                    <td><span class="badge" style="background: {hazard_color};">{forecast.get('hazard_level', 'UNKNOWN').upper()}</span></td>
                    <td>{forecast.get('ros', 0):.1f}</td>
                    <td>{forecast.get('lead_time', 'N/A')} min</td>
                </tr>\n"""
    
    html += f"""            </tbody>
        </table>
        
        <h2>🚨 Operational Recommendations</h2>
        <div class="card">
            <h3>{data.get('recommendations', {}).get('action_level', 'N/A')}</h3>
            <ul>
"""
    
    # Add actions
    for action in data.get('recommendations', {}).get('actions', []):
        html += f"                <li>{action}</li>\n"
    
    html += f"""            </ul>
        </div>
        
        <div class="card">
            <h3>Public Message</h3>
            <div class="alert">
                {data.get('recommendations', {}).get('public_message', 'No public message available')}
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Model:</strong> {data.get('metadata', {}).get('model', 'SYLVA v2.5.0')}</p>
            <p><strong>DOI:</strong> {data.get('metadata', {}).get('doi', '10.5281/zenodo.18627186')}</p>
            <p><strong>Generated:</strong> {data.get('metadata', {}).get('timestamp', 'Unknown')}</p>
            <p>⚠️ This is an automated decision support tool. Always use professional judgment.</p>
        </div>
    </div>
</body>
</html>"""
    
    # Save HTML file
    html_file = json_file.replace('.json', '.html')
    try:
        with open(html_file, 'w') as f:
            f.write(html)
        print(f"✅ HTML report generated: {html_file}")
    except Exception as e:
        print(f"❌ Error saving HTML: {e}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        json_to_html(sys.argv[1])
    else:
        # Find latest report
        reports_dir = Path("reports/daily")
        if reports_dir.exists():
            reports = sorted(reports_dir.glob("*.json"))
            if reports:
                json_to_html(str(reports[-1]))
            else:
                print("❌ No JSON reports found in reports/daily/")
        else:
            print("❌ reports/daily/ directory not found")

if __name__ == "__main__":
    main()
