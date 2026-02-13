#!/bin/bash
# SYLVA - تنظيم ملفات Netlify Dashboard

echo "🔥 SYLVA - تنظيم ملفات Netlify Dashboard"
echo "========================================="

# إنشاء هيكل المجلدات
mkdir -p public/{css,js,assets,assets/icons,assets/data}
mkdir -p scripts config docs data

# إنشاء ملف بيانات تجريبي
cat > data/latest_report.json << 'EOJ'
{
  "metadata": {
    "model": "SYLVA v2.5",
    "doi": "10.5281/zenodo.18627186",
    "region": "Attica, Greece",
    "timestamp": "2026-02-13T10:30:00",
    "fuel_types": ["Pinus halepensis", "Quercus ilex", "Maquis", "Grassland"]
  },
  "summary": {
    "risk": {
      "score": 72,
      "level": "VERY HIGH",
      "color": "🔴"
    }
  },
  "forecasts": {
    "pinus_halepensis": {
      "probability": "76.2%",
      "ros": "33.9 m/min",
      "lead_time": "90 min",
      "hazard_level": "WARNING"
    },
    "dry_grassland": {
      "probability": "78.4%",
      "ros": "47.7 m/min",
      "lead_time": "90 min",
      "hazard_level": "WARNING"
    }
  }
}
EOJ
echo "✓ data/latest_report.json created"

# إنشاء README.md
cat > README.md << 'EOF'
# SYLVA - Netlify Deployment

**Operational Intelligence Dashboard for Mediterranean Wildfire Rapid Spread Forecasting**

## 📊 Available Data
- `data/latest_report.json` - Real-time operational report
- `data/historical/` - Case studies (Mati 2018, Pedrógão 2017)

## 🔗 Live Site
https://sylva.netlify.app

## 🔄 Last Update
$(date '+%Y-%m-%d %H:%M UTC')
