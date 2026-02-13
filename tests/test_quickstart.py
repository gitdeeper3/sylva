"""Simple test for SYLVA framework"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sylva import RapidSpreadForecaster


def test_forecaster_initialization():
    """Test that forecaster initializes correctly."""
    forecaster = RapidSpreadForecaster('pinus_halepensis')
    assert forecaster.fuel_type == 'pinus_halepensis'
    print("✅ Forecaster initialization test passed")


def test_basic_prediction():
    """Test that prediction returns expected structure."""
    forecaster = RapidSpreadForecaster('pinus_halepensis')
    result = forecaster.predict(
        lfm=65,
        dfm=6,
        wind_speed=10.4,
        vpd=38.1,
        aspect=225,
        drought_code=487
    )
    
    assert 'probability' in result
    assert 'confidence' in result
    assert 'rsi' in result
    assert 'hazard_level' in result
    assert 0 <= result['probability'] <= 1
    print("✅ Basic prediction test passed")
    print(f"   Probability: {result['probability']:.1%}")
    print(f"   Hazard Level: {result['hazard_level']}")


if __name__ == "__main__":
    print("🧪 Running SYLVA tests...")
    print("=" * 50)
    test_forecaster_initialization()
    test_basic_prediction()
    print("=" * 50)
    print("✅ All tests passed!")
