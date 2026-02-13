#!/system/bin/sh
# SYLVA Daily Reports Runner

echo "🔥 SYLVA Daily Report Generator"
echo "=================================="
echo "Starting daily report generation at $(date)"

# Generate daily report
cd /storage/emulated/0/Download/sylva
python scripts/generate_daily_report.py

# Archive old reports (keep last 30 days)
find reports/daily -name "*.json" -type f -mtime +30 -delete
find reports/daily -name "*.md" -type f -mtime +30 -delete

echo "=================================="
echo "✅ Daily reports completed at $(date)"
