"""
Extraction Accuracy Dashboard - Main Application
A comprehensive dashboard for visualizing extraction accuracy metrics with
responsive design and accessibility features.
"""

import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import dashboard components
from src.data.sample_data import get_sample_data
from src.components.kpi_cards import create_primary_kpi_section
from src.components.gauge_charts import create_primary_gauges_section
from src.components.monthly_carousel import create_monthly_carousel
from src.layouts.main_layout import create_responsive_layout

# Initialize Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Extraction Accuracy Metrics Dashboard"},
        {"name": "theme-color", "content": "#2c3e50"}
    ],
    suppress_callback_exceptions=True
)

# App configuration
app.title = "Extraction Accuracy Dashboard"
server = app.server

# Global data loading
def load_dashboard_data():
    """Load all dashboard data."""
    try:
        primary_metrics, quarterly_data, monthly_data = get_sample_data()
        return primary_metrics, quarterly_data, monthly_data, None
    except Exception as e:
        error_msg = f"Error loading data: {str(e)}"
        print(error_msg)  # Log error
        # Return empty/default data
        return {
            'extraction_accuracy': 0.0,
            'document_accuracy': 0.0,
            'all_fields_accuracy': 0.0
        }, pd.DataFrame(), pd.DataFrame(), error_msg

# Load initial data
primary_metrics, quarterly_data, monthly_data, data_error = load_dashboard_data()

def create_quarterly_trend_chart(quarterly_data: pd.DataFrame) -> go.Figure:
    """Create quarterly trend analysis chart."""
    if quarterly_data.empty:
        # Return empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            text="No quarterly data available",
            showarrow=False,
            font={'size': 16, 'color': 'gray'},
            xref="paper", yref="paper"
        )
        fig.update_layout(
            height=400,
            xaxis={'visible': False},
            yaxis={'visible': False},
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig
    
    fig = go.Figure()
    
    # Add traces for each field
    fields = ['field_1_accuracy', 'field_2_accuracy', 'field_3_accuracy']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    names = ['Field 1', 'Field 2', 'Field 3']
    
    for field, color, name in zip(fields, colors, names):
        if field in quarterly_data.columns:
            fig.add_trace(go.Scatter(
                x=quarterly_data['quarter'],
                y=quarterly_data[field],
                mode='lines+markers',
                name=name,
                line=dict(color=color, width=3),
                marker=dict(size=8, color=color),
                hovertemplate=f'<b>{name}</b><br>Quarter: %{{x}}<br>Accuracy: %{{y}}%<extra></extra>'
            ))
    
    fig.update_layout(
        title=dict(
            text="Quarterly Field Accuracy Trends",
            font={'size': 20, 'family': 'Inter, Arial, sans-serif'}
        ),
        xaxis_title="Quarter",
        yaxis_title="Accuracy (%)",
        height=500,  # Increased height
        width=None,  # Let it be responsive
        margin=dict(l=60, r=60, t=80, b=60),  # Increased margins
        font={'family': 'Inter, Arial, sans-serif', 'size': 12},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,1)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,  # Move legend below chart
            xanchor="center",
            x=0.5
        ),
        hovermode='x unified',
        autosize=True  # Enable autosizing
    )
    
    # Add grid and styling
    fig.update_xaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(
        showgrid=True, 
        gridcolor='rgba(128,128,128,0.2)',
        range=[75, 100]  # Focus on relevant accuracy range
    )
    
    return fig

def create_monthly_heatmap(monthly_data: pd.DataFrame) -> go.Figure:
    """Create monthly performance heatmap."""
    if monthly_data.empty:
        # Return empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            text="No monthly data available",
            showarrow=False,
            font={'size': 16, 'color': 'gray'},
            xref="paper", yref="paper"
        )
        fig.update_layout(
            height=400,
            xaxis={'visible': False},
            yaxis={'visible': False},
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig
    
    # Prepare data for heatmap
    try:
        heatmap_data = monthly_data.pivot_table(
            values='field_1_accuracy',
            index='year',
            columns='month',
            aggfunc='mean'
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=[f"Month {i}" for i in heatmap_data.columns],
            y=heatmap_data.index,
            colorscale='RdYlGn',
            zmin=75,
            zmax=100,
            colorbar=dict(title="Accuracy (%)"),
            hovertemplate='Year: %{y}<br>%{x}<br>Accuracy: %{z:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text="Monthly Field 1 Accuracy Heatmap",
                font={'size': 20, 'family': 'Inter, Arial, sans-serif'}
            ),
            xaxis_title="Month",
            yaxis_title="Year",
            height=450,  # Increased height
            margin=dict(l=60, r=60, t=80, b=60),
            font={'family': 'Inter, Arial, sans-serif', 'size': 12},
            autosize=True
        )
        
    except Exception as e:
        print(f"Error creating heatmap: {e}")
        # Fallback to simple bar chart
        fig = px.bar(
            monthly_data.tail(12),
            x='date',
            y='field_1_accuracy',
            title="Recent Monthly Performance",
            labels={'date': 'Month', 'field_1_accuracy': 'Field 1 Accuracy (%)'}
        )
        fig.update_layout(height=400)
    
    return fig

# Create dashboard components
def create_dashboard_layout():
    """Create the complete dashboard layout."""
    try:
        # Create components
        kpi_section = create_primary_kpi_section(primary_metrics)
        gauge_charts = create_primary_gauges_section(primary_metrics)
        monthly_carousel = create_monthly_carousel(
            monthly_data=monthly_data,
            selected_quarter="Q1-2025"
        )
        
        # Return layout
        return create_responsive_layout(
            primary_metrics=primary_metrics,
            kpi_section=kpi_section,
            gauge_charts=gauge_charts,
            monthly_carousel=monthly_carousel
        )
    except Exception as e:
        print(f"Error creating dashboard layout: {e}")
        # Return error layout
        return html.Div([
            html.H1("Dashboard Error", className="text-center text-danger"),
            html.P(f"Error: {str(e)}", className="text-center"),
            html.P("Please check that all dependencies are installed.", className="text-center")
        ], className="container mt-5")

# Create main layout
app.layout = create_dashboard_layout()

# Callbacks for interactivity
@app.callback(
    Output("offcanvas-sidebar", "is_open"),
    Input("sidebar-toggle", "n_clicks"),
    State("offcanvas-sidebar", "is_open"),
)
def toggle_offcanvas(n_clicks, is_open):
    """Toggle sidebar navigation."""
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    [Output("loading-output", "children"),
     Output("metrics-store", "data")],
    Input("refresh-btn", "n_clicks")
)
def refresh_dashboard_data(n_clicks):
    """Refresh dashboard data when refresh button is clicked."""
    if n_clicks:
        try:
            new_primary_metrics, _, _, error = load_dashboard_data()
            if error:
                return html.Div(f"Error: {error}", className="alert alert-danger"), primary_metrics
            return html.Div("Data refreshed successfully!", className="alert alert-success"), new_primary_metrics
        except Exception as e:
            return html.Div(f"Refresh failed: {str(e)}", className="alert alert-danger"), primary_metrics
    return "", primary_metrics

@app.callback(
    Output("export-btn", "href"),
    Input("export-btn", "n_clicks")
)
def generate_export_link(n_clicks):
    """Generate CSV export link."""
    if n_clicks:
        # In a real application, this would generate and serve a CSV file
        return "data:text/csv;charset=utf-8,metric,value\\nExtraction Accuracy,94.2\\nDocument Accuracy,91.8"
    return ""


# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Inter', 'Arial', sans-serif;
                background-color: #f8f9fa;
            }
            .dashboard-container {
                min-height: 100vh;
            }
            .gauge-chart, .quarterly-chart, .monthly-chart {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 1rem;
                margin-bottom: 2rem;
                min-height: 400px;
            }
            
            .quarterly-chart {
                min-height: 550px;
            }
            
            .monthly-chart {
                min-height: 500px;
            }
            
            /* Monthly Carousel Styling */
            .monthly-carousel-container {
                padding: 2rem 1rem;
            }
            
            .carousel-wrapper {
                min-height: 400px;
                padding: 1rem 0;
            }
            
            .month-card {
                transition: all 0.3s ease;
                height: 100%;
            }
            
            .month-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.15) !important;
            }
            
            /* Ensure consistent card heights */
            .month-card .card {
                height: 100%;
                display: flex;
                flex-direction: column;
            }
            
            .month-card .card-body {
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            
            .carousel-indicator {
                transition: all 0.2s ease;
            }
            
            .carousel-indicator:hover {
                transform: scale(1.2);
            }
            @media (max-width: 768px) {
                .dashboard-container {
                    padding: 0.5rem;
                }
                h1 {
                    font-size: 1.8rem !important;
                }
                h3 {
                    font-size: 1.4rem !important;
                }
            }
            /* Accessibility improvements */
            .btn:focus, .form-select:focus, .form-control:focus {
                box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
            }
            /* High contrast mode support */
            @media (prefers-contrast: high) {
                .card {
                    border: 2px solid !important;
                }
                .btn {
                    border: 2px solid !important;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    # Development server configuration
    debug_mode = os.environ.get('DASH_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 8050))
    
    print(f"🚀 Starting Extraction Accuracy Dashboard on port {port}")
    print(f"📊 Dashboard URL: http://localhost:{port}")
    
    if data_error:
        print(f"⚠️  Warning: {data_error}")
    
    app.run(
        debug=debug_mode,
        host='127.0.0.1',
        port=port,
        dev_tools_ui=debug_mode,
        dev_tools_props_check=debug_mode
    )