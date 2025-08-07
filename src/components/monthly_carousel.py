"""
Monthly Carousel component for displaying monthly accuracy data in a quarter.
Shows month-by-month data with navigation controls and KPI-style cards.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime


def create_month_card(
    month_name: str,
    month_data: Dict[str, float],
    is_active: bool = False
) -> dbc.Card:
    """
    Create a single month card showing accuracy metrics.
    
    Args:
        month_name: Name of the month (e.g., "January 2025")
        month_data: Dictionary with field accuracies
        is_active: Whether this card is currently active
    
    Returns:
        Bootstrap Card component
    """
    # Determine overall status based on average accuracy
    field_values = [v for v in month_data.values() if isinstance(v, (int, float))]
    avg_accuracy = sum(field_values) / len(field_values) if field_values else 0
    
    # Color coding
    if avg_accuracy >= 90:
        card_color = 'success'
        text_color = 'white'
        status_text = 'Excellent'
        status_icon = '🟢'
    elif avg_accuracy >= 75:
        card_color = 'warning'  
        text_color = 'dark'
        status_text = 'Good'
        status_icon = '🟡'
    else:
        card_color = 'danger'
        text_color = 'white'
        status_text = 'Bad'
        status_icon = '🔴'
    
    # Add active state styling
    card_class = "h-100 shadow-sm month-card"
    if is_active:
        card_class += " border-primary"
        card_style = {'borderWidth': '3px'}
    else:
        card_style = {}
    
    # Create field accuracy items
    field_items = []
    for field_name, accuracy in month_data.items():
        if isinstance(accuracy, (int, float)):
            field_items.append(
                html.Div([
                    html.Span(field_name.replace('_', ' ').title(), className="text-muted small"),
                    html.H6(f"{accuracy:.1f}%", className="mb-0 fw-bold")
                ], className="d-flex justify-content-between align-items-center mb-1")
            )
    
    card_content = [
        html.Div([
            html.H5([
                status_icon, " ", month_name
            ], className="card-title text-center mb-2"),
            html.P(f"Average: {avg_accuracy:.1f}%", 
                   className="text-center h4 fw-bold mb-3"),
            html.P(status_text, className="text-center fw-bold mb-3"),
            html.Hr(),
            html.Div(field_items, className="field-details")
        ])
    ]
    
    return dbc.Card(
        dbc.CardBody(card_content),
        color=card_color,
        className=card_class,
        style=card_style
    )


def create_monthly_carousel(
    monthly_data: pd.DataFrame,
    selected_quarter: str = "Q1-2025",
    field_columns: List[str] = None
) -> html.Div:
    """
    Create monthly carousel component for a specific quarter.
    
    Args:
        monthly_data: DataFrame with monthly data
        selected_quarter: Quarter to show (e.g., "Q1-2025")
        field_columns: List of field column names to display
    
    Returns:
        HTML Div containing the carousel
    """
    if field_columns is None:
        field_columns = ['field_1_accuracy', 'field_2_accuracy', 'field_3_accuracy']
    
    # Filter data for selected quarter
    if not monthly_data.empty and 'quarter' in monthly_data.columns:
        quarter_data = monthly_data[monthly_data['quarter'] == selected_quarter.split('-')[0]]
        
        # If we have year info, filter by year too
        if 'year' in monthly_data.columns and '-' in selected_quarter:
            year = int(selected_quarter.split('-')[1])
            quarter_data = quarter_data[quarter_data['year'] == year]
    else:
        quarter_data = pd.DataFrame()
    
    if quarter_data.empty:
        # Create sample data for the selected quarter
        quarter_data = create_sample_quarter_data(selected_quarter, field_columns)
    
    # Create month cards
    month_cards = []
    month_names = []
    
    # Determine months for the quarter
    quarter_num = selected_quarter.split('-')[0].replace('Q', '')
    year = selected_quarter.split('-')[1] if '-' in selected_quarter else '2025'
    
    quarter_months = {
        '1': ['January', 'February', 'March'],
        '2': ['April', 'May', 'June'], 
        '3': ['July', 'August', 'September'],
        '4': ['October', 'November', 'December']
    }
    
    months = quarter_months.get(quarter_num, ['January', 'February', 'March'])
    
    for i, month_name in enumerate(months):
        month_display = f"{month_name} {year}"
        month_names.append(month_display)
        
        # Get data for this month
        if not quarter_data.empty:
            month_num = i + 1 + (int(quarter_num) - 1) * 3
            month_row = quarter_data[quarter_data['month'] == month_num]
            
            if not month_row.empty:
                month_data = {}
                for field in field_columns:
                    if field in month_row.columns:
                        month_data[field] = month_row.iloc[0][field]
            else:
                month_data = create_sample_month_data(field_columns)
        else:
            month_data = create_sample_month_data(field_columns)
        
        # Create card
        card = create_month_card(
            month_name=month_display,
            month_data=month_data,
            is_active=(i == 0)  # First month is active by default
        )
        
        month_cards.append(
            dbc.Col(
                card, 
                id=f"month-card-{i}", 
                width=12, 
                md=6, 
                lg=4,
                className="mb-3"
            )
        )
    
    return html.Div([
        # Title only
        html.Div([
            html.H3("Monthly Performance Overview", 
                   className="mb-4 text-center",
                   style={'fontSize': '1.6rem', 'color': '#34495e'})
        ]),
        
        # Carousel content
        html.Div([
            dbc.Row(
                month_cards, 
                id="carousel-container",
                className="g-3 justify-content-center"
            )
        ], className="carousel-wrapper"),
        
        
    ], id="monthly-carousel", className="monthly-carousel-container")


def create_sample_quarter_data(quarter: str, field_columns: List[str]) -> pd.DataFrame:
    """Create sample data for a quarter when real data is not available."""
    import random
    
    quarter_num = int(quarter.split('-')[0].replace('Q', ''))
    year = int(quarter.split('-')[1]) if '-' in quarter else 2025
    
    data = []
    for month_offset in range(3):
        month = (quarter_num - 1) * 3 + month_offset + 1
        
        row = {
            'year': year,
            'month': month,
            'quarter': f'Q{quarter_num}'
        }
        
        # Generate sample field accuracies
        for field in field_columns:
            base_accuracy = 85 + random.random() * 10  # 85-95%
            row[field] = round(base_accuracy, 1)
        
        data.append(row)
    
    return pd.DataFrame(data)


def create_sample_month_data(field_columns: List[str]) -> Dict[str, float]:
    """Create sample month data when real data is not available."""
    import random
    
    data = {}
    for field in field_columns:
        base_accuracy = 80 + random.random() * 15  # 80-95%
        data[field] = round(base_accuracy, 1)
    
    return data