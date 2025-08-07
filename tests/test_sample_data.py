"""
Tests for sample data generation functionality.
"""

import pytest
import pandas as pd
from src.data.sample_data import MetricsDataGenerator, get_sample_data


class TestMetricsDataGenerator:
    """Test the MetricsDataGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = MetricsDataGenerator()
    
    def test_generate_primary_metrics(self):
        """Test primary metrics generation."""
        metrics = self.generator.generate_primary_metrics()
        
        # Check required keys
        assert 'extraction_accuracy' in metrics
        assert 'document_accuracy' in metrics
        assert 'all_fields_accuracy' in metrics
        
        # Check value ranges
        for value in metrics.values():
            assert isinstance(value, float)
            assert 0 <= value <= 100
    
    def test_generate_quarterly_data(self):
        """Test quarterly data generation."""
        data = self.generator.generate_quarterly_data()
        
        # Check DataFrame structure
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
        assert 'quarter' in data.columns
        assert 'field_1_accuracy' in data.columns
        assert 'field_2_accuracy' in data.columns
        assert 'field_3_accuracy' in data.columns
        
        # Check data types and ranges
        for field in ['field_1_accuracy', 'field_2_accuracy', 'field_3_accuracy']:
            assert data[field].dtype in ['float64', 'int64']
            assert all(0 <= value <= 100 for value in data[field])
    
    def test_generate_monthly_data(self):
        """Test monthly data generation."""
        data = self.generator.generate_monthly_data()
        
        # Check DataFrame structure
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
        assert 'year' in data.columns
        assert 'month' in data.columns
        assert 'quarter' in data.columns
        assert 'field_1_accuracy' in data.columns
        
        # Check data ranges
        assert all(1 <= month <= 12 for month in data['month'])
        assert all(2020 <= year <= 2025 for year in data['year'])
    
    def test_get_accuracy_color(self):
        """Test accuracy color coding."""
        assert self.generator.get_accuracy_color(98) == 'green'
        assert self.generator.get_accuracy_color(92) == 'yellow'
        assert self.generator.get_accuracy_color(85) == 'red'
    
    def test_get_accuracy_status(self):
        """Test accuracy status text."""
        assert self.generator.get_accuracy_status(98) == 'Excellent'
        assert self.generator.get_accuracy_status(92) == 'Good'
        assert self.generator.get_accuracy_status(85) == 'Needs Improvement'
        assert self.generator.get_accuracy_status(75) == 'Critical'


def test_get_sample_data():
    """Test the convenience function."""
    primary_metrics, quarterly_data, monthly_data = get_sample_data()
    
    # Check primary metrics
    assert isinstance(primary_metrics, dict)
    assert len(primary_metrics) == 3
    
    # Check quarterly data
    assert isinstance(quarterly_data, pd.DataFrame)
    assert len(quarterly_data) > 0
    
    # Check monthly data
    assert isinstance(monthly_data, pd.DataFrame)
    assert len(monthly_data) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])