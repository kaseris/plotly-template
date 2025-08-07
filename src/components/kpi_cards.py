"""
KPI Cards component for displaying primary extraction accuracy metrics.
Features responsive design with color-coded backgrounds and trend indicators.
"""

from dash import html
import dash_bootstrap_components as dbc
from typing import Dict, Optional


def create_kpi_card(
    title: str,
    value: float,
    subtitle: Optional[str] = None,
    trend: Optional[str] = None,
    color_threshold: Optional[Dict[str, float]] = None
) -> dbc.Card:
    """
    Create a single KPI card with value, trend, and color coding.
    
    Args:
        title: Card title
        value: Primary metric value
        subtitle: Optional subtitle text
        trend: Optional trend indicator ('up', 'down', 'stable')
        color_threshold: Color coding thresholds {'excellent': 95, 'good': 90}
    
    Returns:
        Dash Bootstrap Components Card
    """
    if color_threshold is None:
        color_threshold = {'excellent': 95, 'good': 90}
    
    # Determine card color based on value
    if value >= color_threshold['excellent']:
        card_color = 'success'
        text_color = 'white'
    elif value >= color_threshold['good']:
        card_color = 'warning'
        text_color = 'dark'
    else:
        card_color = 'danger'
        text_color = 'white'
    
    # Trend icon
    trend_icon = ""
    if trend == 'up':
        trend_icon = "↗️"
    elif trend == 'down':
        trend_icon = "↘️"
    elif trend == 'stable':
        trend_icon = "→"
    
    # Card content
    card_body = [
        html.H4(title, className="card-title text-center mb-2", 
                style={'fontSize': '1.1rem', 'fontWeight': '600'}),
        html.Div([
            html.H1(f"{value}%", 
                    className="text-center mb-1",
                    style={'fontSize': '2.5rem', 'fontWeight': 'bold', 'lineHeight': '1'}),
            html.P(trend_icon, className="text-center mb-0", style={'fontSize': '1.2rem'})
        ], className="d-flex flex-column align-items-center"),
    ]
    
    if subtitle:
        card_body.append(
            html.P(subtitle, className="card-text text-center small",
                   style={'fontSize': '0.85rem', 'opacity': '0.9'})
        )
    
    return dbc.Card(
        dbc.CardBody(card_body),
        color=card_color,
        className="h-100 shadow-sm",
        style={
            'minHeight': '160px',
            'border': 'none',
            'borderRadius': '8px'
        }
    )


def create_primary_kpi_section(primary_metrics: Dict[str, float]) -> html.Div:
    """
    Create the primary KPI cards section with all three main metrics.
    
    Args:
        primary_metrics: Dictionary with extraction accuracy metrics
    
    Returns:
        HTML Div containing responsive KPI cards
    """
    # Define card configurations
    kpi_configs = [
        {
            'key': 'extraction_accuracy',
            'title': 'Extraction Accuracy',
            'subtitle': 'Overall system performance'
        },
        {
            'key': 'document_accuracy',
            'title': 'Document Accuracy',
            'subtitle': 'Document-level success'
        },
        {
            'key': 'all_fields_accuracy',
            'title': 'All Fields Accuracy',
            'subtitle': 'Complete field extraction'
        }
    ]
    
    # Create KPI cards
    kpi_cards = []
    for config in kpi_configs:
        value = primary_metrics.get(config['key'], 0.0)
        
        # Simple trend simulation (in real app, this would come from historical data)
        trend = 'up' if value > 90 else 'stable' if value > 85 else 'down'
        
        card = create_kpi_card(
            title=config['title'],
            value=value,
            subtitle=config['subtitle'],
            trend=trend
        )
        kpi_cards.append(dbc.Col(card, width=12, md=4, className="mb-3"))
    
    return html.Div([
        html.H2("Key Performance Indicators", 
                className="mb-4 text-center",
                style={'fontSize': '1.8rem', 'fontWeight': '600', 'color': '#2c3e50'}),
        dbc.Row(kpi_cards, className="g-3")
    ], className="mb-5")


def create_summary_stats_card(quarterly_data, monthly_data) -> dbc.Card:
    """
    Create a summary statistics card with additional insights.
    
    Args:
        quarterly_data: DataFrame with quarterly metrics
        monthly_data: DataFrame with monthly metrics
    
    Returns:
        Summary statistics card
    """
    try:
        # Calculate some basic stats
        latest_quarter = quarterly_data.iloc[-1]
        avg_field_1 = quarterly_data['field_1_accuracy'].mean()
        avg_field_2 = quarterly_data['field_2_accuracy'].mean()
        avg_field_3 = quarterly_data['field_3_accuracy'].mean()
        
        # Recent monthly trend (last 3 months)
        recent_months = monthly_data.tail(3)
        trend_field_1 = "improving" if recent_months['field_1_accuracy'].is_monotonic_increasing else "stable"
        
        stats_content = [
            html.H5("Performance Insights", className="card-title mb-3"),
            html.Ul([
                html.Li(f"Latest Quarter: {latest_quarter['quarter']}"),
                html.Li(f"Field 1 Average: {avg_field_1:.1f}%"),
                html.Li(f"Field 2 Average: {avg_field_2:.1f}%"),
                html.Li(f"Field 3 Average: {avg_field_3:.1f}%"),
                html.Li(f"Recent Trend: {trend_field_1.title()}")
            ], className="list-unstyled")
        ]
        
    except Exception as e:
        stats_content = [
            html.H5("Performance Insights", className="card-title mb-3"),
            html.P("Statistics will be available once data is loaded.", 
                   className="text-muted")
        ]
    
    return dbc.Card(
        dbc.CardBody(stats_content),
        className="shadow-sm",
        style={'borderRadius': '8px'}
    )