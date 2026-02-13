# Contributing to SYLVA

First off, thank you for considering contributing to SYLVA! Your help is essential for improving operational wildfire forecasting in Mediterranean systems.

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Workflow](#development-workflow)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

This project is committed to providing a welcoming, inclusive, and harassment-free experience for everyone. We expect all contributors to:

- Be respectful and considerate
- Use inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

**Unacceptable behavior** will not be tolerated and may result in permanent exclusion from the project.

---

## 🚀 Getting Started

### Prerequisites
```bash
# Fork the repository on GitLab
# Then clone your fork
git clone https://gitlab.com/your-username/sylva.git
cd sylva

# Set up upstream remote
git remote add upstream https://gitlab.com/gitdeeper3/sylva.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
pre-commit install
```

---

💡 How Can I Contribute?

🐛 Priority 1: Bug Fixes

· Report bugs via GitLab Issues
· Fix confirmed bugs in core modules
· Improve error handling and logging

🔬 Priority 2: Scientific Development

· Enhanced LFM retrieval: Improve Sentinel-2 NDWI algorithms
· DFM sensor integration: Develop drivers for in-situ moisture sensors
· New fuel types: Add Eucalyptus, Fynbos, Chaparral
· Climate adaptation: RCP4.5/RCP8.5 scenario calibration

📊 Priority 3: Validation

· Add new case studies from recent fires
· Expand validation database to North America
· Improve uncertainty quantification
· Develop cross-validation frameworks

🌍 Priority 4: Operational Tools

· Real-time data assimilation
· Mobile app development
· Web interface improvements
· Alert system enhancements

📚 Priority 5: Documentation

· Tutorial creation
· API documentation
· Translation to Mediterranean languages
· Video demonstrations

---

🔄 Development Workflow

Branch Naming Convention

```
feature/    - New features (e.g., feature/ensemble-forecasting)
bugfix/     - Bug fixes (e.g., bugfix/rsi-calculation-error)
docs/       - Documentation (e.g., docs/api-reference-update)
validation/ - Validation studies (e.g., validation/california-2025)
research/   - Experimental research (e.g., research/lstm-prediction)
```

Commit Message Format

```
type(scope): Brief description

Detailed description of changes, reasons, and impact.

Closes #ISSUE_NUMBER
```

Types: feat, fix, docs, style, refactor, perf, test, chore, validation

Example:

```
feat(core): Add ensemble forecasting with 50 members

- Implemented Monte Carlo dropout for uncertainty quantification
- Added parallel processing for member generation
- Created ensemble visualization module
- Updated probability calibration for ensemble inputs

Closes #142
```

---

🎨 Style Guidelines

Python (PEP 8)

```python
# ✅ Good
def calculate_rapid_spread_index(
    lfm: float,
    dfm: float,
    wind_speed: float,
    fuel_type: str = "pinus_halepensis"
) -> float:
    """Calculate Rapid Spread Index from environmental parameters."""
    return weighted_sum(normalized_params)

# ❌ Bad
def calc_rsi(l,d,w,ft):
    return wsum(norm([l,d,w]))
```

Docstrings (Google Style)

```python
def predict_probability(
    rsi: float,
    confidence: float = 1.0
) -> Dict[str, float]:
    """
    Calculate rapid spread probability using logistic regression.
    
    Args:
        rsi: Rapid Spread Index (0-100)
        confidence: Forecast confidence multiplier (0-1)
    
    Returns:
        Dictionary containing:
        - probability: Rapid spread probability (0-1)
        - calibrated_prob: Bias-corrected probability
    
    Raises:
        ValueError: If rsi is outside valid range
    """
```

Type Hints

Always use type hints for function parameters and return values.

---

🧪 Testing

Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_core/test_rothermel.py

# Run with coverage
pytest --cov=sylva tests/

# Run performance benchmarks
pytest tests/benchmarks/
```

Writing Tests

```python
# ✅ Good test
def test_rapid_spread_high_wind():
    """Test rapid spread detection under high wind conditions."""
    forecaster = RapidSpreadForecaster(fuel_type="grassland")
    result = forecaster.predict(wind_speed=15.0, lfm=60, dfm=5)
    assert result["probability"] > 0.7
    assert result["confidence"] > 0.8

# Required coverage: Minimum 80% for core modules
```

---

📚 Documentation

Building Documentation

```bash
cd docs
pip install -r requirements-docs.txt
make html
open _build/html/index.html
```

Documentation Standards

· docstrings: Every public function and class
· notebooks: Tutorials for each major feature
· examples: Runnable example scripts
· user guide: Clear, step-by-step instructions

---

🐛 Issue Reporting

Bug Report Template

```markdown
**Describe the bug**
Clear description of the issue.

**To Reproduce**
Steps to reproduce the behavior:
1. Initialize forecaster with '...'
2. Call predict() with parameters '...'
3. See error

**Expected behavior**
What should have happened.

**Environment:**
- OS: [e.g., Ubuntu 22.04, Termux Android 14]
- Python version: [e.g., 3.9.7]
- SYLVA version: [e.g., 0.1.0]
- Dependencies: [output of pip freeze]

**Additional context**
Error logs, screenshots, or relevant data.
```

Feature Request Template

```markdown
**Problem statement**
What problem does this feature solve?

**Proposed solution**
How should it work?

**Alternative solutions**
Other approaches considered.

**Additional context**
References to similar systems or research papers.
```

---

🔀 Pull Request Process

Before Submitting

1. Update documentation for any changed functionality
2. Add tests for new features
3. Run full test suite: pytest tests/
4. Check code style: flake8 sylva/
5. Update CHANGELOG.md with your changes
6. Ensure CI pipeline passes (GitLab CI)

PR Title Format

```
[Type] Brief description (Closes #ISSUE)
```

Example: [FEAT] Ensemble forecasting with 50 members (Closes #142)

PR Description Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/passed
- [ ] Integration tests added/passed
- [ ] Manual testing completed

## Validation
- POD improvement: +X%
- FAR reduction: -Y%
- Lead time: Z minutes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have updated the documentation
- [ ] I have added tests
- [ ] All tests pass locally
- [ ] CHANGELOG.md is updated

## Related Issues
Closes #[issue_number]
```

---

🎖 Recognition

Contributors will be:

· Added to AUTHORS.md
· Mentioned in release notes
· Credited in research publications (where applicable)
· Invited to join as project members (after significant contributions)

---

📧 Questions?

· GitLab Issues: For bugs and feature requests
· GitLab Discussions: For general questions
· Email: gitdeeper@gmail.com (project lead)
· Matrix: #sylva-project:matrix.org

---

🚨 Urgent Issues

For critical security vulnerabilities or operational safety issues:

1. Do not open a public issue
2. Email directly: gitdeeper@gmail.com
3. Encrypt with GPG key: [0x...]

---

Thank you for contributing to safer Mediterranean communities through better wildfire forecasting!

- The SYLVA Team
