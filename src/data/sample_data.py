"""
Sample data generators for extraction accuracy metrics dashboard.
Provides realistic sample data with seasonal variations and trends.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class MetricsDataGenerator:
    """Generate sample extraction accuracy metrics data."""
    
    def __init__(self, base_accuracy: float = 90.0, seasonal_variation: float = 5.0):
        """
        Initialize data generator.
        
        Args:
            base_accuracy: Base accuracy percentage (default: 90.0)
            seasonal_variation: Maximum seasonal variation in percentage (default: 5.0)
        """
        self.base_accuracy = base_accuracy
        self.seasonal_variation = seasonal_variation
        np.random.seed(42)  # For reproducible data
    
    def generate_primary_metrics(self) -> Dict[str, float]:
        """Generate current primary metrics."""
        # Add some realistic variations
        return {
            'extraction_accuracy': round(self.base_accuracy + np.random.normal(2, 1), 1),
            'document_accuracy': round(self.base_accuracy + np.random.normal(0, 1.5), 1),
            'all_fields_accuracy': round(self.base_accuracy + np.random.normal(-2, 2), 1)
        }
    
    def generate_quarterly_data(self, num_quarters: int = 8) -> pd.DataFrame:
        """
        Generate quarterly accuracy data for multiple fields.
        
        Args:
            num_quarters: Number of quarters to generate (default: 8)
        
        Returns:
            DataFrame with quarterly data
        """
        quarters = []
        field_1_data = []
        field_2_data = []
        field_3_data = []
        
        # Start from 2 years ago
        current_year = datetime.now().year
        start_year = current_year - 2
        
        for i in range(num_quarters):
            year = start_year + (i // 4)
            quarter = (i % 4) + 1
            quarters.append(f"Q{quarter}-{year}")
            
            # Simulate improving trend over time with some noise
            trend_improvement = i * 1.5  # Gradual improvement
            seasonal_factor = 2 * np.sin(2 * np.pi * i / 4)  # Seasonal variation
            
            # Field 1: Generally best performing
            field_1_accuracy = (self.base_accuracy + trend_improvement + seasonal_factor + 
                               np.random.normal(2, 1))
            field_1_data.append(round(min(field_1_accuracy, 98.0), 1))
            
            # Field 2: Moderate performance
            field_2_accuracy = (self.base_accuracy + trend_improvement + seasonal_factor + 
                               np.random.normal(0, 1.2))
            field_2_data.append(round(min(field_2_accuracy, 97.0), 1))
            
            # Field 3: More challenging field
            field_3_accuracy = (self.base_accuracy + trend_improvement + seasonal_factor + 
                               np.random.normal(-3, 1.5))
            field_3_data.append(round(max(min(field_3_accuracy, 95.0), 75.0), 1))
        
        return pd.DataFrame({
            'quarter': quarters,
            'field_1_accuracy': field_1_data,
            'field_2_accuracy': field_2_data,
            'field_3_accuracy': field_3_data
        })
    
    def generate_monthly_data(self, num_months: int = 24) -> pd.DataFrame:
        """
        Generate monthly accuracy data for detailed drill-down.
        
        Args:
            num_months: Number of months to generate (default: 24)
        
        Returns:
            DataFrame with monthly data
        """
        data = []
        
        # Start from 2 years ago
        current_date = datetime.now()
        start_date = current_date.replace(year=current_date.year - 2, month=1, day=1)
        
        for i in range(num_months):
            date = start_date + timedelta(days=30 * i)
            year = date.year
            month = date.month
            quarter = f"Q{((month - 1) // 3) + 1}"
            
            # Monthly variations with trends
            monthly_trend = i * 0.8  # Gradual improvement
            monthly_seasonal = 3 * np.sin(2 * np.pi * i / 12)  # Annual seasonality
            random_variation = np.random.normal(0, 2)
            
            # Generate field accuracies
            base_monthly = self.base_accuracy + monthly_trend + monthly_seasonal
            
            field_1 = round(min(base_monthly + np.random.normal(3, 1.5), 98.5), 1)
            field_2 = round(min(base_monthly + np.random.normal(1, 1.8), 97.5), 1)
            field_3 = round(max(min(base_monthly + np.random.normal(-2, 2.2), 96.0), 75.0), 1)
            
            data.append({
                'year': year,
                'month': month,
                'month_name': date.strftime('%B'),
                'quarter': quarter,
                'date': date.strftime('%Y-%m'),
                'field_1_accuracy': field_1,
                'field_2_accuracy': field_2,
                'field_3_accuracy': field_3
            })
        
        return pd.DataFrame(data)
    
    def get_accuracy_color(self, accuracy: float) -> str:
        """
        Get color based on accuracy thresholds.
        
        Args:
            accuracy: Accuracy percentage
        
        Returns:
            Color string (green, yellow, red)
        """
        if accuracy >= 90:  # Excellent
            return 'green'
        elif accuracy >= 75:  # Good
            return 'yellow'
        else:  # Bad
            return 'red'
    
    def get_accuracy_status(self, accuracy: float) -> str:
        """
        Get status text based on accuracy.
        
        Args:
            accuracy: Accuracy percentage
        
        Returns:
            Status string
        """
        if accuracy >= 90:
            return 'Excellent'
        elif accuracy >= 75:
            return 'Good'
        else:
            return 'Bad'


def get_sample_data() -> Tuple[Dict, pd.DataFrame, pd.DataFrame]:
    """
    Convenience function to get all sample data.
    
    Returns:
        Tuple of (primary_metrics, quarterly_data, monthly_data)
    """
    generator = MetricsDataGenerator()
    
    primary_metrics = generator.generate_primary_metrics()
    quarterly_data = generator.generate_quarterly_data()
    monthly_data = generator.generate_monthly_data()
    
    return primary_metrics, quarterly_data, monthly_data


if __name__ == "__main__":
    # Demo the data generation
    generator = MetricsDataGenerator()
    
    print("Primary Metrics:")
    print(generator.generate_primary_metrics())
    
    print("\nQuarterly Data (last 5 rows):")
    print(generator.generate_quarterly_data().tail())
    
    print("\nMonthly Data (last 5 rows):")
    print(generator.generate_monthly_data().tail())