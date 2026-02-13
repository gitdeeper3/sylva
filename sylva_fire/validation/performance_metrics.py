"""Performance metrics for validation"""

import numpy as np
from typing import Dict


class PerformanceMetrics:
    """Calculate standard verification metrics."""
    
    def __init__(self):
        self.confusion_matrix = {
            'hits': 0,
            'false_alarms': 0,
            'misses': 0,
            'correct_negatives': 0
        }
    
    def calculate_contingency(self, observed: np.ndarray, forecasted: np.ndarray, threshold: float = 0.5):
        """Calculate contingency table."""
        forecast_binary = (forecasted >= threshold).astype(int)
        
        self.confusion_matrix['hits'] = np.sum((forecast_binary == 1) & (observed == 1))
        self.confusion_matrix['false_alarms'] = np.sum((forecast_binary == 1) & (observed == 0))
        self.confusion_matrix['misses'] = np.sum((forecast_binary == 0) & (observed == 1))
        self.confusion_matrix['correct_negatives'] = np.sum((forecast_binary == 0) & (observed == 0))
        
        return self.confusion_matrix
    
    def calculate_pod(self) -> float:
        """Probability of Detection."""
        total = self.confusion_matrix['hits'] + self.confusion_matrix['misses']
        if total == 0:
            return np.nan
        return self.confusion_matrix['hits'] / total
    
    def calculate_far(self) -> float:
        """False Alarm Ratio."""
        total = self.confusion_matrix['hits'] + self.confusion_matrix['false_alarms']
        if total == 0:
            return np.nan
        return self.confusion_matrix['false_alarms'] / total
    
    def calculate_csi(self) -> float:
        """Critical Success Index."""
        denominator = (self.confusion_matrix['hits'] + 
                      self.confusion_matrix['misses'] + 
                      self.confusion_matrix['false_alarms'])
        if denominator == 0:
            return np.nan
        return self.confusion_matrix['hits'] / denominator
    
    def calculate_all_metrics(self, observed: np.ndarray, probabilities: np.ndarray, threshold: float = 0.5) -> Dict:
        """Calculate all verification metrics."""
        self.calculate_contingency(observed, probabilities, threshold)
        
        return {
            'POD': self.calculate_pod(),
            'FAR': self.calculate_far(),
            'CSI': self.calculate_csi(),
            'hits': self.confusion_matrix['hits'],
            'false_alarms': self.confusion_matrix['false_alarms'],
            'misses': self.confusion_matrix['misses'],
            'correct_negatives': self.confusion_matrix['correct_negatives']
        }
