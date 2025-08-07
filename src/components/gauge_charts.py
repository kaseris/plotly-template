"""
Gauge Charts component for visualizing accuracy metrics with color-coded thresholds.
Uses Plotly's Indicator component to create accessible and responsive gauge visualizations.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from typing import Dict, List, Optional, Tuple


def create_gauge_chart(
    value: float,
    title: str,
    max_value: float = 100.0,
    thresholds: Optional[Dict[str, float]] = None,
    size: Tuple[int, int] = (300, 250)
) -> go.Figure:
    """
    Create a single gauge chart with color-coded thresholds.
    
    Args:
        value: Current metric value
        title: Chart title
        max_value: Maximum value for the gauge (default: 100.0)
        thresholds: Color thresholds {'excellent': 90, 'good': 75, 'bad': 0}
        size: Chart size as (width, height)
    
    Returns:
        Plotly Figure with gauge chart
    """
    if thresholds is None:
        thresholds = {'excellent': 90, 'good': 75, 'bad': 0}
    
    # Determine gauge color and status based on new thresholds
    if value >= thresholds['excellent']:
        gauge_color = '#28a745'  # Green
        status_text = 'Excellent'
    elif value >= thresholds['good']:
        gauge_color = '#ffc107'  # Yellow
        status_text = 'Good'
    else:
        gauge_color = '#dc3545'  # Red
        status_text = 'Bad'
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 18, 'family': 'Arial, sans-serif'}},
        gauge={
            'axis': {
                'range': [0, max_value],
                'tickwidth': 1,
                'tickcolor': "#333"
            },
            'bar': {'color': gauge_color, 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#ccc",
            'steps': [
                {'range': [0, thresholds['good']], 'color': '#ffebee'},  # Bad: 0-75
                {'range': [thresholds['good'], thresholds['excellent']], 'color': '#fff3cd'},  # Good: 75-90
                {'range': [thresholds['excellent'], max_value], 'color': '#d4edda'}  # Excellent: 90+
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': thresholds['excellent']
            }
        }
    ))
    
    # Add status annotation - positioned lower to avoid overlap
    fig.add_annotation(
        x=0.5, y=-0.1,  # Moved lower 
        text=f"<b>{status_text}</b>",
        showarrow=False,
        font={'size': 14, 'color': gauge_color, 'family': 'Arial, sans-serif'},
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor=gauge_color,
        borderwidth=1,
        borderpad=4
    )
    
    fig.update_layout(
        width=size[0],
        height=size[1],
        margin=dict(l=20, r=20, t=60, b=40),  # Increased bottom margin for annotation
        font={'color': "#333", 'family': 'Arial, sans-serif'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig


def create_primary_gauges_section(primary_metrics: Dict[str, float]) -> Dict[str, go.Figure]:
    """
    Create gauge charts for all primary metrics.
    
    Args:
        primary_metrics: Dictionary with extraction accuracy metrics
    
    Returns:
        Dictionary of gauge charts keyed by metric name
    """
    gauge_configs = [
        {
            'key': 'extraction_accuracy',
            'title': 'Extraction Accuracy',
            'thresholds': {'excellent': 90, 'good': 75, 'bad': 0}
        },
        {
            'key': 'document_accuracy',
            'title': 'Document Accuracy',
            'thresholds': {'excellent': 90, 'good': 75, 'bad': 0}
        },
        {
            'key': 'all_fields_accuracy',
            'title': 'All Fields Accuracy',
            'thresholds': {'excellent': 90, 'good': 75, 'bad': 0}
        }
    ]
    
    gauges = {}
    for config in gauge_configs:
        value = primary_metrics.get(config['key'], 0.0)
        gauges[config['key']] = create_gauge_chart(
            value=value,
            title=config['title'],
            thresholds=config['thresholds'],
            size=(350, 280)
        )
    
    return gauges


def create_compact_gauge(
    value: float,
    title: str,
    max_value: float = 100.0,
    color: Optional[str] = None
) -> go.Figure:
    """
    Create a compact gauge chart for smaller displays.
    
    Args:
        value: Current metric value
        title: Chart title
        max_value: Maximum value for the gauge
        color: Custom color for the gauge
    
    Returns:
        Compact Plotly Figure
    """
    if color is None:
        if value >= 90:  # Excellent
            color = '#28a745'
        elif value >= 75:  # Good
            color = '#ffc107'
        else:  # Bad
            color = '#dc3545'
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 14}},
        gauge={
            'axis': {'range': [0, max_value], 'tickwidth': 1},
            'bar': {'color': color, 'thickness': 0.4},
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#ddd"
        }
    ))
    
    fig.update_layout(
        width=200,
        height=150,
        margin=dict(l=10, r=10, t=40, b=10),
        font={'color': "#333", 'size': 12},
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig


def create_multi_gauge_dashboard(metrics_dict: Dict[str, float]) -> go.Figure:
    """
    Create a multi-gauge dashboard in a single figure.
    
    Args:
        metrics_dict: Dictionary of metric names and values
    
    Returns:
        Combined gauge chart figure
    """
    num_gauges = len(metrics_dict)
    cols = min(3, num_gauges)  # Maximum 3 columns
    rows = (num_gauges + cols - 1) // cols  # Calculate required rows
    
    # Create subplot titles
    subplot_titles = list(metrics_dict.keys())
    
    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=subplot_titles,
        specs=[[{'type': 'indicator'}] * cols for _ in range(rows)]
    )
    
    for i, (metric_name, value) in enumerate(metrics_dict.items()):
        row = (i // cols) + 1
        col = (i % cols) + 1
        
        # Determine color
        if value >= 90:  # Excellent
            color = '#28a745'
        elif value >= 75:  # Good
            color = '#ffc107'
        else:  # Bad
            color = '#dc3545'
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=value,
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color},
                    'bgcolor': "white",
                    'borderwidth': 1,
                    'bordercolor': "#ddd"
                }
            ),
            row=row, col=col
        )
    
    fig.update_layout(
        height=300 * rows,
        margin=dict(l=20, r=20, t=60, b=20),
        font={'color': "#333"},
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig


def create_horizontal_bar_chart(metrics_dict: Dict[str, float]) -> go.Figure:
    """
    Alternative visualization as horizontal bar chart for accessibility.
    
    Args:
        metrics_dict: Dictionary of metric names and values
    
    Returns:
        Horizontal bar chart figure
    """
    metrics = list(metrics_dict.keys())
    values = list(metrics_dict.values())
    
    # Color coding based on values
    colors = []
    for value in values:
        if value >= 90:  # Excellent
            colors.append('#28a745')
        elif value >= 75:  # Good
            colors.append('#ffc107')
        else:  # Bad
            colors.append('#dc3545')
    
    fig = go.Figure(go.Bar(
        x=values,
        y=metrics,
        orientation='h',
        marker=dict(color=colors),
        text=[f'{v}%' for v in values],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Arial'),
        hovertemplate='<b>%{y}</b><br>Accuracy: %{x}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Accuracy Metrics Overview",
        xaxis_title="Accuracy (%)",
        yaxis_title="",
        height=len(metrics) * 80 + 100,
        margin=dict(l=20, r=20, t=60, b=40),
        font={'color': "#333", 'family': 'Arial, sans-serif'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            showgrid=False
        )
    )
    
    # Add reference lines
    fig.add_vline(x=90, line_dash="dash", line_color="green", 
                  annotation_text="Excellent", annotation_position="top")
    fig.add_vline(x=75, line_dash="dash", line_color="orange", 
                  annotation_text="Good", annotation_position="top")
    
    return fig