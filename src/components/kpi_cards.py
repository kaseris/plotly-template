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
    Create a compact KPI card with light theme styling.
    
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
    
    # Light theme color determination with subtle backgrounds
    if value >= color_threshold['excellent']:
        card_style = {
            'backgroundColor': '#d1edff',  # Light blue background
            'borderLeft': '4px solid #0d6efd',
            'color': '#212529'
        }
        badge_color = 'primary'
    elif value >= color_threshold['good']:
        card_style = {
            'backgroundColor': '#d4f6d4',  # Light green background
            'borderLeft': '4px solid #198754',
            'color': '#212529'
        }
        badge_color = 'success'
    else:
        card_style = {
            'backgroundColor': '#ffeaa7',  # Light yellow background
            'borderLeft': '4px solid #ffc107',
            'color': '#212529'
        }
        badge_color = 'warning'
    
    # Compact trend icon
    trend_icon = ""
    trend_text = ""
    if trend == 'up':
        trend_icon = "▲"
        trend_text = "Improving"
    elif trend == 'down':
        trend_icon = "▼"
        trend_text = "Declining"
    elif trend == 'stable':
        trend_icon = "■"
        trend_text = "Stable"
    
    # Compact card content
    card_body = [
        html.Div([
            html.H5(title, className="mb-1", 
                    style={'fontSize': '0.9rem', 'fontWeight': '600', 'color': '#212529'}),
            html.Div([
                html.Span(f"{value}%", 
                         className="fw-bold",
                         style={'fontSize': '1.8rem', 'color': '#212529'}),
                dbc.Badge([trend_icon, f" {trend_text}"], 
                         color=badge_color, 
                         className="ms-2",
                         style={'fontSize': '0.7rem'})
            ], className="d-flex align-items-center justify-content-between")
        ])
    ]
    
    if subtitle:
        card_body.append(
            html.P(subtitle, className="text-muted mb-0 mt-1",
                   style={'fontSize': '0.75rem'})
        )
    
    return dbc.Card(
        dbc.CardBody(card_body, className="py-2 px-3"),
        className="h-100",
        style={
            **card_style,
            'minHeight': '100px',
            'border': '1px solid #dee2e6',
            'borderRadius': '6px'
        }
    )


def create_primary_kpi_section(primary_metrics: Dict[str, float]) -> html.Div:
    """
    Create compact primary KPI cards section with light theme styling.
    
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
            'subtitle': 'Overall performance'
        },
        {
            'key': 'document_accuracy',
            'title': 'Document Accuracy',
            'subtitle': 'Document success'
        },
        {
            'key': 'all_fields_accuracy',
            'title': 'All Fields Accuracy',
            'subtitle': 'Complete extraction'
        }
    ]
    
    # Create compact KPI cards
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
        kpi_cards.append(dbc.Col(card, width=12, sm=6, lg=4, className="mb-2"))
    
    return html.Div([
        html.H2("Overall Extraction Accuracy", 
                className="mb-2 h5 text-center",
                style={'fontWeight': '600', 'color': '#212529'}),
        dbc.Row(kpi_cards, className="g-2")
    ], className="mb-3")


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