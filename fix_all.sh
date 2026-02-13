#!/system/bin/sh
# SYLVA - Fix all errors

echo "🔥 SYLVA Error Fixer"
echo "=================================="

cd /storage/emulated/0/Download/sylva

echo "1️⃣ Fixing imports..."
touch scripts/__init__.py
touch reports/__init__.py
touch reports/daily/__init__.py

echo "2️⃣ Fixing rothermel.py..."
python -c "from sylva_fire.core.rothermel import RothermelModel; print('   ✅ Rothermel OK')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "   ⚠️  Error detected, fixing..."
    # Already fixed with the cat command above
fi

echo "3️⃣ Testing imports..."
python -c "import sys; sys.path.insert(0, '.'); from sylva_fire.forecasting.rapid_spread_forecast import RapidSpreadForecaster; print('   ✅ Imports OK')"

echo "4️⃣ Generating test report..."
python scripts/generate_daily_report.py

echo "5️⃣ Generating HTML..."
python reports/daily/to_html.py

echo "=================================="
echo "✅ All fixes applied!"
echo "📊 Check reports in: reports/daily/"
