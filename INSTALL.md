# Installation Guide

## 📋 Prerequisites

### System Requirements
- **OS**: Linux, macOS, Windows (WSL2), Android (Termux)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB for base installation, 10GB for full dataset
- **Python**: 3.8 or higher

### Dependencies
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev gdal-bin libgdal-dev

# macOS
brew install python3 gdal

# Termux (Android)
pkg install python python-pip gdal
```

🚀 Installation Methods

Method 1: PyPI (Coming Soon)

```bash
pip install sylva-fire
```

Method 2: From Source

```bash
git clone https://gitlab.com/gitdeeper3/sylva.git
cd sylva
pip install -e .
```

Method 3: Docker

```bash
docker pull gitdeeper3/sylva:latest
docker run -it sylva:latest
```

🔧 Development Installation

```bash
pip install -e ".[dev]"
pre-commit install
```

✅ Verify Installation

```bash
python -c "import sylva; print(sylva.__version__)"
```

📊 Download Validation Database

```bash
python scripts/download_validation_data.py
```

