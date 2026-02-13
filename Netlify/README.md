# 🔥 SYLVA - Operational Intelligence Dashboard

**Mediterranean Wildfire Rapid Spread Forecasting System**

[![Netlify Status](https://api.netlify.com/api/v1/badges/your-badge/deploy-status)](https://sylva.netlify.app)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18627186.svg)](https://doi.org/10.5281/zenodo.18627186)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## 📋 Overview

SYLVA Netlify Dashboard is the **command center interface** for the SYLVA Operational Intelligence System. It provides real-time visualization of wildfire rapid spread risk, WUI evacuation decisions, and resource requirements for Mediterranean civil protection agencies.

### Live Demo
🔗 **https://sylva.netlify.app**

---

## 🚀 Quick Deploy

### 1. Clone & Install
```bash
git clone https://gitlab.com/gitdeeper3/sylva.git
cd sylva/Netlify
npm install
```

2. Run Locally

```bash
npm start
# Opens http://localhost:8080/dashboard.html
```

3. Deploy to Netlify

```bash
npm run deploy
# or
netlify deploy --prod
```

---

📁 Project Structure

```
Netlify/
├── public/                      # Static files
│   ├── dashboard.html          # Main command center
│   ├── css/
│   │   └── style.css          # Dashboard styling
│   ├── js/
│   │   └── dashboard.js       # Interactive features
│   └── assets/
│       ├── icons/             # UI icons
│       └── data/             # Cached reports
│
├── functions/                  # Serverless APIs
│   ├── weather.js            # OpenWeatherMap
│   ├── sentinel.js           # Sentinel-2 LFM
│   ├── cffdrs.js            # Drought Code
│   └── sylva-forecast.js    # SYLVA engine
│
├── data/                      # Data cache
│   └── latest_report.json    # Current operational report
│
├── config/                    # Configuration
│   └── api-keys.js          # API credentials
│
├── scripts/                   # Utilities
│   └── update-report.js     # Fetch latest SYLVA report
│
├── netlify.toml             # Deployment config
├── package.json             # Dependencies
├── organize.sh             # Project setup
└── README.md               # This file
```

---

📊 Data Sources

Source Parameter Update Frequency
OpenWeatherMap Wind, VPD, Temperature 10 minutes
Sentinel-2 LFM (Live Fuel Moisture) 5 days
CFFDRS Drought Code, FFMC Daily
Copernicus DEM Aspect, Slope Static
SYLVA Engine Risk Score, ROS, WUI On-demand

---

🔌 API Endpoints

Endpoint Description Response
/api/weather Real-time weather data JSON
/api/lfm Live Fuel Moisture JSON
/api/forecast Complete SYLVA forecast JSON
/data/latest_report.json Cached operational report JSON

---

🎯 Dashboard Features

✅ Command Center View

· Risk Level Indicator - ⚫🔴🟠🟡🟢 with score
· WUI Evacuation Decision - Immediate, Prepare, Warning, Monitor
· Fire Behavior Matrix - ROS, Probability, Lead Time by fuel type
· Containment Assessment - Difficulty, Success Probability
· Resource Requirements - Crews, Engines, Air Tankers, Cost
· Seasonal Context - Drought percentile analysis

✅ Real-time Updates

· Auto-refresh every 10 minutes
· Live weather integration
· Latest SYLVA forecast

---

🔧 Development

Local Testing

```bash
# Install dependencies
npm install

# Start local server
npm start

# Update with latest SYLVA report
npm run update
```

Environment Variables

Create .env file:

```bash
OPENWEATHER_API_KEY=your_key
SENTINEL_CLIENT_ID=your_id
SENTINEL_CLIENT_SECRET=your_secret
```

---

📈 Performance

Metric Value
Dashboard Load Time < 1.5s
API Response Time < 300ms
Cache TTL 3600s
Concurrent Users 1000+

---

📚 Case Studies

🔥 Mati Fire, Greece (2018)

· Detection: 75 minutes before rapid spread
· WUI Arrival: 31 minutes (dashboard prediction)
· Evacuation Decision: 🟠 PREPARE FOR EVACUATION

🔥 Pedrógão Grande, Portugal (2017)

· Detection: 90 minutes before rapid spread
· Crown Fire Potential: 🔴 95% - VERY HIGH
· Containment: 🔴 VERY DIFFICULT

---

🤝 Contributing

1. Fork the repository
2. Create your feature branch (git checkout -b feature/amazing-feature)
3. Commit changes (git commit -m 'Add amazing feature')
4. Push to branch (git push origin feature/amazing-feature)
5. Open a Merge Request

---

📄 License

Creative Commons Attribution 4.0 International (CC BY 4.0)

---

👤 Author

Samir Baladi

· Email: gitdeeper@gmail.com
· ORCID: 0009-0003-8903-0029
· GitLab: @gitdeeper3
· DOI: 10.5281/zenodo.18627186

---

🙏 Acknowledgments

· Mediterranean Civil Protection Agencies
· European Forest Fire Information System (EFFIS)
· Canadian Forest Service (CFFDRS)
· European Space Agency (Sentinel-2)

---

⚠️ Disclaimer

SYLVA is an operational decision support tool. Always use professional judgment and consider multiple information sources. Not a substitute for operational expertise and local knowledge.

---

🔥 SYLVA v2.5 - Operational Intelligence for Mediterranean Wildfire Rapid Spread Forecasting
📅 Last Updated: February 13, 2026
🔗 DOI: 10.5281/zenodo.18627186

---

Deployed with ❤️ on Netlify
