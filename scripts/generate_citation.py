#!/usr/bin/env python3
"""Generate citation in multiple formats."""

import sys
import os

# Add parent directory to path for relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sylva import __version__, __doi__, __author__

def generate_bibtex():
    """Generate BibTeX citation."""
    return f"""@software{{baladi2026sylva,
  author       = {{Baladi, Samir}},
  title        = {{SYLVA: A Thermodynamic-Fuel Continuum Framework for Wildfire Spread Rate Estimation in Mediterranean Forest Systems}},
  year         = 2026,
  version      = {{{__version__}}},
  doi          = {{{__doi__}}},
  url          = {{https://doi.org/10.5281/zenodo.18627186}},
  publisher    = {{Zenodo}},
  license      = {{CC-BY-4.0}}
}}"""

def generate_apa():
    """Generate APA citation."""
    return f"Baladi, S. (2026). SYLVA: A Thermodynamic-Fuel Continuum Framework for Wildfire Spread Rate Estimation in Mediterranean Forest Systems (Version {__version__}) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.18627186"

def generate_ris():
    """Generate RIS citation."""
    return f"""TY  - COMP
AU  - Baladi, Samir
PY  - 2026
TI  - SYLVA: A Thermodynamic-Fuel Continuum Framework for Wildfire Spread Rate Estimation in Mediterranean Forest Systems
T2  - Zenodo
VL  - {__version__}
DO  - 10.5281/zenodo.18627186
UR  - https://zenodo.org/records/18627186
ER  -"""

if __name__ == "__main__":
    print("=" * 60)
    print("SYLVA Citation Generator")
    print("=" * 60)
    print(f"\n📋 DOI: {__doi__}")
    print(f"📦 Version: {__version__}")
    print(f"👤 Author: {__author__}")
    
    print("\n📚 BibTeX:")
    print("-" * 40)
    print(generate_bibtex())
    
    print("\n📚 APA:")
    print("-" * 40)
    print(generate_apa())
    
    print("\n📚 RIS:")
    print("-" * 40)
    print(generate_ris())
    
    # Save to file
    with open("CITATION.bib", "w") as f:
        f.write(generate_bibtex())
    print("\n✅ BibTeX saved to CITATION.bib")
