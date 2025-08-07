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
    
    # Add traces for each field with consistent light theme colors
    fields = ['field_1_accuracy', 'field_2_accuracy', 'field_3_accuracy']
    colors = ['#0d6efd', '#198754', '#ffc107']  # Light theme colors: blue, success, warning
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
            font={'size': 16, 'family': 'Inter, sans-serif', 'color': '#212529'}
        ),
        xaxis_title="Quarter",
        yaxis_title="Accuracy (%)",
        height=380,  # Compact height
        margin=dict(l=40, r=20, t=50, b=40),  # Compact margins
        font={'family': 'Inter, sans-serif', 'size': 11, 'color': '#212529'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font={'size': 10}
        ),
        hovermode='x unified',
        autosize=True
    )
    
    # Add grid and styling with light theme
    fig.update_xaxes(
        showgrid=True, 
        gridcolor='#e9ecef',
        gridwidth=1,
        linecolor='#dee2e6'
    )
    fig.update_yaxes(
        showgrid=True, 
        gridcolor='#e9ecef',
        gridwidth=1,
        linecolor='#dee2e6',
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
                font={'size': 16, 'family': 'Inter, sans-serif', 'color': '#212529'}
            ),
            xaxis_title="Month",
            yaxis_title="Year",
            height=350,  # Compact height
            margin=dict(l=40, r=20, t=50, b=40),  # Compact margins
            font={'family': 'Inter, sans-serif', 'size': 11, 'color': '#212529'},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#ffffff",
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

@app.callback(
    [Output("dashboard-container", "className"),
     Output("accessibility-state", "data"),
     Output("normal-theme-btn", "active"),
     Output("high-contrast-btn", "active"),
     Output("text-small-btn", "active"),
     Output("text-normal-btn", "active"),
     Output("text-large-btn", "active")],
    [Input("normal-theme-btn", "n_clicks"),
     Input("high-contrast-btn", "n_clicks"),
     Input("text-small-btn", "n_clicks"),
     Input("text-normal-btn", "n_clicks"),
     Input("text-large-btn", "n_clicks"),
     Input("accessibility-features", "value")],
    State("accessibility-state", "data")
)
def update_accessibility_settings(normal_clicks, contrast_clicks, small_clicks, 
                                normal_text_clicks, large_clicks, features, current_state):
    """Handle accessibility settings changes."""
    if current_state is None:
        current_state = {
            "high_contrast": False,
            "text_size": "normal",
            "screen_reader_mode": False,
            "colorblind_mode": False
        }
    
    ctx = dash.callback_context
    if not ctx.triggered:
        # Initial load - ensure light theme
        base_classes = "dashboard-container light-theme"
        return (base_classes, current_state, 
                True, False, False, True, False)  # Normal theme and text active
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Handle theme buttons
    if button_id == "normal-theme-btn":
        current_state["high_contrast"] = False
    elif button_id == "high-contrast-btn":
        current_state["high_contrast"] = True
    
    # Handle text size buttons
    elif button_id == "text-small-btn":
        current_state["text_size"] = "small"
    elif button_id == "text-normal-btn":
        current_state["text_size"] = "normal"
    elif button_id == "text-large-btn":
        current_state["text_size"] = "large"
    
    # Handle additional features
    if features:
        current_state["screen_reader_mode"] = "screen_reader_mode" in features
        current_state["colorblind_mode"] = "colorblind_mode" in features
    else:
        current_state["screen_reader_mode"] = False
        current_state["colorblind_mode"] = False
    
    # Build CSS classes - ensure light theme is default
    classes = ["dashboard-container", "light-theme"]
    
    if current_state.get("high_contrast", False):
        classes.append("high-contrast-mode")
    
    text_size = current_state.get("text_size", "normal")
    classes.append(f"text-size-{text_size}")
    
    if current_state.get("colorblind_mode", False):
        classes.append("colorblind-friendly")
    
    if current_state.get("screen_reader_mode", False):
        classes.append("screen-reader-mode")
    
    # Button active states
    theme_normal_active = not current_state.get("high_contrast", False)
    theme_contrast_active = current_state.get("high_contrast", False)
    text_small_active = text_size == "small"
    text_normal_active = text_size == "normal"
    text_large_active = text_size == "large"
    
    return (" ".join(classes), current_state,
            theme_normal_active, theme_contrast_active,
            text_small_active, text_normal_active, text_large_active)

@app.callback(
    Output("keyboard-shortcuts-modal", "is_open"),
    [Input("keyboard-shortcuts-btn", "n_clicks"),
     Input("close-shortcuts-modal", "n_clicks")],
    State("keyboard-shortcuts-modal", "is_open")
)
def toggle_shortcuts_modal(open_clicks, close_clicks, is_open):
    """Toggle keyboard shortcuts modal."""
    ctx = dash.callback_context
    if ctx.triggered:
        return not is_open
    return is_open


# Add custom CSS - Compact Light Theme
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                /* Light Theme Color Palette */
                --bg-primary: #ffffff;
                --bg-secondary: #f8f9fa;
                --bg-light: #e9ecef;
                --text-primary: #212529;
                --text-secondary: #6c757d;
                --text-muted: #adb5bd;
                --border-light: #dee2e6;
                --border-medium: #ced4da;
                --accent-blue: #0d6efd;
                --accent-success: #198754;
                --accent-warning: #ffc107;
                --accent-danger: #dc3545;
                --shadow-light: rgba(0,0,0,0.05);
                --shadow-medium: rgba(0,0,0,0.1);
                
                /* Compact spacing variables */
                --spacing-xs: 0.25rem;
                --spacing-sm: 0.5rem;
                --spacing-md: 0.75rem;
                --spacing-lg: 1rem;
                --spacing-xl: 1.5rem;
            }

            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background-color: var(--bg-secondary);
                color: var(--text-primary);
                font-size: 14px;
                line-height: 1.4;
            }
            
            /* Ensure light theme is enforced */
            .light-theme,
            .light-theme body,
            .dashboard-container.light-theme {
                background-color: var(--bg-secondary) !important;
                color: var(--text-primary) !important;
            }
            
            .light-theme .card,
            .light-theme .gauge-chart,
            .light-theme .quarterly-chart,
            .light-theme .monthly-chart {
                background-color: var(--bg-primary) !important;
                color: var(--text-primary) !important;
            }
            
            .dashboard-container {
                min-height: 100vh;
                padding: var(--spacing-md) var(--spacing-sm);
            }
            
            /* Compact Cards */
            .card {
                border: 1px solid var(--border-light);
                border-radius: 6px;
                box-shadow: 0 1px 3px var(--shadow-light);
                margin-bottom: var(--spacing-lg);
                transition: box-shadow 0.15s ease;
            }
            
            .card:hover {
                box-shadow: 0 2px 8px var(--shadow-medium);
            }
            
            .card-body {
                padding: var(--spacing-lg);
            }
            
            .card-header {
                padding: var(--spacing-md) var(--spacing-lg);
                background-color: var(--bg-light);
                border-bottom: 1px solid var(--border-light);
                font-weight: 600;
                font-size: 0.9rem;
            }
            
            /* Compact Charts */
            .gauge-chart, .quarterly-chart, .monthly-chart {
                background-color: var(--bg-primary);
                border-radius: 6px;
                border: 1px solid var(--border-light);
                padding: var(--spacing-md);
                margin-bottom: var(--spacing-lg);
            }
            
            .gauge-chart {
                min-height: 280px;
            }
            
            .quarterly-chart {
                min-height: 380px;
            }
            
            .monthly-chart {
                min-height: 350px;
            }
            
            /* Compact Typography */
            h1 {
                font-size: 1.75rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: var(--spacing-md);
                line-height: 1.2;
            }
            
            h2 {
                font-size: 1.25rem;
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: var(--spacing-sm);
            }
            
            h3 {
                font-size: 1.1rem;
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: var(--spacing-sm);
            }
            
            .text-muted {
                color: var(--text-muted) !important;
                font-size: 0.85rem;
            }
            
            /* Compact Buttons */
            .btn {
                padding: var(--spacing-xs) var(--spacing-md);
                font-size: 0.875rem;
                font-weight: 500;
                border-radius: 4px;
                border: 1px solid transparent;
                transition: all 0.15s ease;
            }
            
            .btn-sm {
                padding: 0.125rem var(--spacing-sm);
                font-size: 0.8rem;
            }
            
            .btn-primary {
                background-color: var(--accent-blue);
                border-color: var(--accent-blue);
                color: white;
            }
            
            .btn-primary:hover {
                background-color: #0b5ed7;
                border-color: #0a58ca;
            }
            
            .btn-outline-secondary {
                border-color: var(--border-medium);
                color: var(--text-secondary);
            }
            
            .btn-outline-secondary:hover {
                background-color: var(--text-secondary);
                color: white;
            }
            
            /* Compact Forms */
            .form-control, .form-select {
                padding: var(--spacing-xs) var(--spacing-sm);
                font-size: 0.875rem;
                border: 1px solid var(--border-medium);
                border-radius: 4px;
                background-color: var(--bg-primary);
            }
            
            .form-label {
                font-size: 0.85rem;
                font-weight: 500;
                color: var(--text-primary);
                margin-bottom: 0.25rem;
            }
            
            /* Compact Monthly Carousel */
            .monthly-carousel-container {
                padding: var(--spacing-lg) var(--spacing-sm);
            }
            
            .carousel-wrapper {
                min-height: 320px;
                padding: var(--spacing-sm) 0;
            }
            
            .month-card {
                transition: all 0.2s ease;
                height: 100%;
            }
            
            .month-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px var(--shadow-medium);
            }
            
            .month-card .card {
                height: 100%;
                border: 1px solid var(--border-light);
            }
            
            .month-card .card-body {
                padding: var(--spacing-md);
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            
            /* Compact Navigation */
            .navbar, .nav {
                padding: var(--spacing-sm) 0;
            }
            
            .nav-link {
                padding: var(--spacing-xs) var(--spacing-md);
                font-size: 0.875rem;
                color: var(--text-secondary);
            }
            
            .nav-link:hover {
                color: var(--accent-blue);
            }
            
            /* Accessibility Toolbar Compact */
            .accessibility-toolbar {
                position: sticky;
                top: var(--spacing-sm);
                z-index: 10;
            }
            
            .accessibility-toolbar .card {
                margin-bottom: var(--spacing-md);
            }
            
            .accessibility-toolbar .btn-group {
                gap: 1px;
            }
            
            .accessibility-toolbar .btn-group .btn {
                padding: 0.125rem 0.375rem;
                font-size: 0.75rem;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .dashboard-container {
                    padding: var(--spacing-sm) var(--spacing-xs);
                }
                
                h1 {
                    font-size: 1.5rem;
                }
                
                .card-body {
                    padding: var(--spacing-md);
                }
                
                .gauge-chart, .quarterly-chart, .monthly-chart {
                    padding: var(--spacing-sm);
                }
            }
            
            @media (max-width: 576px) {
                h1 {
                    font-size: 1.25rem;
                }
                
                .btn {
                    font-size: 0.8rem;
                    padding: 0.125rem var(--spacing-sm);
                }
            }
            
            /* Focus and Accessibility */
            .btn:focus, .form-select:focus, .form-control:focus {
                box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
                outline: none;
            }
            
            /* High contrast support */
            @media (prefers-contrast: high) {
                :root {
                    --border-light: #000000;
                    --border-medium: #000000;
                    --shadow-light: rgba(0,0,0,0.3);
                    --shadow-medium: rgba(0,0,0,0.5);
                }
                
                .card {
                    border: 2px solid var(--border-light);
                }
                
                .btn {
                    border-width: 2px;
                }
            }
            
            /* Reduced motion support */
            @media (prefers-reduced-motion: reduce) {
                .month-card, .card, .btn {
                    transition: none;
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