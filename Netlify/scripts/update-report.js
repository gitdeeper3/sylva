const fs = require('fs');
const path = require('path');

// نسخ آخر تقرير من reports/daily/ إلى Netlify/data/
const reportsDir = path.join(__dirname, '../../reports/daily');
const targetDir = path.join(__dirname, '../data');

// تأكد من وجود المجلد
if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
}

// الحصول على آخر ملف JSON
if (fs.existsSync(reportsDir)) {
    const files = fs.readdirSync(reportsDir)
        .filter(f => f.endsWith('.json') && !f.includes('template'))
        .sort()
        .reverse();

    if (files.length > 0) {
        const latest = files[0];
        fs.copyFileSync(
            path.join(reportsDir, latest),
            path.join(targetDir, 'latest_report.json')
        );
        console.log(`✅ Copied ${latest} to Netlify/data/latest_report.json`);
    } else {
        console.log('⚠️ No report files found');
    }
} else {
    console.log('⚠️ Reports directory not found');
}
