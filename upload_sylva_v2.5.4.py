import requests
import hashlib
import os

TOKEN = "pypi-AgEIcHlwaS5vcmcCJDU1ZWNmMmUwLWE4NGUtNDYyZS1hYzY1LTE3M2QwZTMxNGMyMwACKlszLCJlZjQ3ZDllOS04YmU5LTQ2OWMtYWQ0OC0wODRhZTg4YzZjMTUiXQAABiCt0SR8PPPMEQEHWMSjvTPGfrncRynVuL_a5G8NAfVsmw"

def upload_file(filepath, filetype):
    filename = os.path.basename(filepath)
    print(f"📤 رفع {filename}...")
    
    with open(filepath, 'rb') as f:
        content = f.read()
        md5 = hashlib.md5(content).hexdigest()
        sha256 = hashlib.sha256(content).hexdigest()
    
    with open(filepath, 'rb') as f:
        files = {'content': (filename, f)}
        data = {
            ':action': 'file_upload',
            'protocol_version': '1',
            'metadata_version': '2.1',
            'name': 'sylva-fire',
            'version': '2.5.4',
            'summary': '🔥 Thermodynamic-Fuel Continuum Framework for Wildfire Spread Rate Estimation in Mediterranean Forest Systems',
            'author': 'Samir Baladi',
            'author_email': 'gitdeeper@gmail.com',
            'license': 'CC-BY-4.0',
            'keywords': 'wildfire,mediterranean,fire-spread,rothermel,operational-intelligence,wui,evacuation',
            'home_page': 'https://gitlab.com/gitdeeper3/sylva',
            'description': open('README.md', 'r', encoding='utf-8').read(),
            'description_content_type': 'text/markdown',
            'classifier': [
                'Development Status :: 4 - Beta',
                'Intended Audience :: Science/Research',
                'Intended Audience :: Emergency Services',
                'License :: OSI Approved :: Creative Commons Attribution 4.0 International (CC BY 4.0)',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9',
                'Programming Language :: Python :: 3.10',
                'Topic :: Scientific/Engineering :: Atmospheric Science',
                'Topic :: Scientific/Engineering :: GIS',
                'Operating System :: OS Independent',
            ],
            'requires_python': '>=3.8',
            'filetype': filetype,
            'md5_digest': md5,
            'sha256_digest': sha256,
        }
        
        if filetype == 'bdist_wheel':
            data['pyversion'] = 'py3'
        else:
            data['pyversion'] = 'source'
        
        response = requests.post(
            'https://upload.pypi.org/legacy/',
            files=files,
            data=data,
            auth=('__token__', TOKEN)
        )
    
    print(f"  الحالة: {response.status_code}")
    if response.status_code == 200:
        print(f"  ✅ نجاح!")
    else:
        print(f"  ❌ خطأ: {response.text[:200]}")
    return response.status_code == 200

# رفع الملفات
print("🚀 رفع sylva-fire v2.5.4 مع الوصف الكامل...")

files = [
    ("dist/sylva_fire-2.5.4-py3-none-any.whl", "bdist_wheel"),
    ("dist/sylva_fire-2.5.4.tar.gz", "sdist")
]

success = True
for filepath, filetype in files:
    if os.path.exists(filepath):
        if not upload_file(filepath, filetype):
            success = False
        print()
    else:
        print(f"❌ الملف غير موجود: {filepath}")
        success = False

if success:
    print("🎉 تم رفع v2.5.4 بنجاح!")
    print("⏳ انتظر 3-5 دقائق، ثم تحقق:")
    print("   https://pypi.org/project/sylva-fire/2.5.4/")
else:
    print("⚠️ فشل رفع بعض الملفات")
