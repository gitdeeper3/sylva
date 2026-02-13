import requests, hashlib, os, glob

TOKEN = "pypi-AgEIcHlwaS5vcmcCJDU1ZWNmMmUwLWE4NGUtNDYyZS1hYzY1LTE3M2QwZTMxNGMyMwACKlszLCJlZjQ3ZDllOS04YmU5LTQ2OWMtYWQ0OC0wODRhZTg4YzZjMTUiXQAABiCt0SR8PPPMEQEHWMSjvTPGfrncRynVuL_a5G8NAfVsmw"

tar_files = glob.glob("dist/sylva_fire-*.tar.gz")
if not tar_files:
    print("❌ لا توجد ملفات sylva_fire في مجلد dist/")
    exit(1)

filepath = tar_files[0]
filename = os.path.basename(filepath)
version = "2.5.4"  # إصدار جديد

print("="*60)
print("📦 SYLVA FIRE - رفع على PyPI")
print("="*60)
print(f"📤 الملف: {filename}")
print(f"📌 الإصدار: {version}")
print("="*60)

with open(filepath, 'rb') as f:
    content = f.read()

# الوصف الكامل والمباشر
description = """
SYLVA Fire: Thermodynamic-Fuel Continuum Framework for Wildfire Spread Rate Estimation in Mediterranean Forest Systems

🔴 KEY FEATURES:
• Rapid Spread Index (RSI): Nine-parameter integration (LFM, DFM, CBD, SFL, FBD, Vw, VPD, Aspect, DC)
• Operational Dashboard: Color-coded command center interface with real-time risk assessment
• Quantitative Risk Score: 0-100 scale with 6-factor calculation (DFM, Wind, VPD, DC, Crown, Containment)
• WUI Evacuation Timing: Precise arrival calculations with ±2 minutes accuracy (Mati 2018: 31 min)
• Threat Zone Modeling: Elliptical fire growth model (width/length = 0.25, 92ha threat zone)
• Driver Ranking: Visual percentage bars with top 3 risk factors
• Containment Probability: Success rate, optimal window, and resource estimation

📊 PERFORMANCE (213 Mediterranean wildfires, 2000-2024):
• Probability of Detection (POD): 0.83 (81-87% accuracy)
• False Alarm Ratio (FAR): 0.16 (31-43% reduction vs operational guidance)
• Critical Success Index (CSI): 0.71
• Brier Skill Score: 0.36
• WUI Arrival Accuracy: ±2 minutes vs documented cases
• Dashboard Generation: <0.5 seconds

🔥 FUEL TYPE PERFORMANCE:
• Pinus halepensis (68 cases): POD 0.86 (+15% vs BehavePlus)
• Quercus ilex (42 cases): POD 0.81 (+14% vs BehavePlus)
• Mediterranean maquis (53 cases): POD 0.84 (+15% vs BehavePlus)
• Dry grassland (24 cases): POD 0.79 (+22% vs BehavePlus)

🎯 OPERATIONAL DECISION THRESHOLDS:
• 80-100 EXTREME (⚫) - IMMEDIATE EVACUATION - Type 1 IMT
• 65-79 VERY HIGH (🔴) - PREPARE FOR EVACUATION - Type 1 IMT
• 50-64 HIGH (🟠) - EVACUATION WARNING - Type 2 IMT
• 35-49 MODERATE (🟡) - MONITOR - Type 3 IMT
• 0-34 LOW (🟢) - ROUTINE - Type 4/5 IMT

📚 CITATION:
Baladi, S. (2026). SYLVA: Operational Intelligence System for Mediterranean Wildfire Rapid Spread Forecasting (Version 2.5.0). Zenodo. https://doi.org/10.5281/zenodo.18627186

🔗 LINKS:
• Documentation: https://sylva-fire.readthedocs.io
• Source Code: https://gitlab.com/gitdeeper3/sylva
• DOI: 10.5281/zenodo.18627186

📦 INSTALLATION:
pip install sylva-fire

🚀 QUICK START:
from sylva_fire.operational import Dashboard
dashboard = Dashboard()
report = dashboard.generate_report(region="Attica, Greece")
print(report.risk_level)  # "VERY HIGH"

⚠️ LICENSE: Creative Commons Attribution 4.0 International (CC-BY 4.0)
"""

data = {
    ':action': 'file_upload',
    'metadata_version': '2.1',
    'name': 'sylva-fire',
    'version': version,
    'filetype': 'sdist',
    'pyversion': 'source',
    'md5_digest': hashlib.md5(content).hexdigest(),
    'sha256_digest': hashlib.sha256(content).hexdigest(),
    'description': description,  # الوصف المباشر
    'description_content_type': 'text/plain',
    'summary': 'Thermodynamic-Fuel Continuum Framework for Wildfire Spread Rate Estimation in Mediterranean Forest Systems',
    'keywords': 'wildfire, mediterranean, fire-spread, rothermel, operational-intelligence, wui, evacuation',
    'author': 'Samir Baladi',
    'author_email': 'gitdeeper@gmail.com',
    'license': 'CC-BY-4.0',
    'platform': 'any',
    'classifiers': 'Programming Language :: Python :: 3, Programming Language :: Python :: 3.8, Programming Language :: Python :: 3.9, Programming Language :: Python :: 3.10, License :: OSI Approved :: Creative Commons Attribution 4.0 International (CC BY 4.0), Operating System :: OS Independent, Topic :: Scientific/Engineering :: Atmospheric Science, Topic :: Scientific/Engineering :: GIS, Intended Audience :: Science/Research, Intended Audience :: Emergency Services',
}

print("🚀 جاري الرفع إلى PyPI مع الوصف الكامل...")

with open(filepath, 'rb') as f:
    response = requests.post(
        'https://upload.pypi.org/legacy/',
        files={'content': (filename, f)},
        data=data,
        auth=('__token__', TOKEN),
        timeout=30
    )

print(f"\n📊 الحالة: {response.status_code}")
if response.status_code == 200:
    print("✅ ✅ ✅ تم الرفع بنجاح مع الوصف!")
    print(f"\n🎉 الحزمة متاحة الآن:")
    print(f"🔗 https://pypi.org/project/sylva-fire/{version}/")
    print("\n📋 الوصف المُضاف:")
    print("-"*40)
    print(description[:500] + "...")
    print("-"*40)
elif response.status_code == 400 and "already exists" in response.text:
    print("ℹ️  الملف موجود مسبقاً")
else:
    print(f"❌ خطأ: {response.text[:200]}")
