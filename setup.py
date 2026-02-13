from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# قراءة requirements.txt إذا كان موجوداً
try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    requirements = [
        "numpy>=1.19.0",
        "scipy>=1.5.0",
        "pandas>=1.1.0",
        "matplotlib>=3.3.0",
        "scikit-learn>=0.23.0",
    ]

setup(
    name="sylva-fire",
    version="2.5.5",
    author="Samir Baladi",
    author_email="gitdeeper@gmail.com",
    description="Thermodynamic-Fuel Continuum Framework for Wildfire Spread Rate Estimation in Mediterranean Forest Systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gitdeeper3/sylva",
    project_urls={
        "Documentation": "https://sylva-fire.readthedocs.io",
        "Source": "https://gitlab.com/gitdeeper3/sylva",
        "DOI": "https://zenodo.org/records/18627186",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: GIS",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Emergency Services",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)
