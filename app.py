import dash
from dash import html
import dash_bootstrap_components as dbc
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data.sample_data import get_sample_data
from src.components.kpi_cards import create_primary_kpi_section
from src.components.gauge_charts import create_primary_gauges_section
from src.components.monthly_carousel import create_monthly_carousel
from src.layouts.main_layout import create_responsive_layout

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

app.title = "Extraction Accuracy Dashboard"
server = app.server

def load_dashboard_data():
    try:
        primary_metrics, quarterly_data, monthly_data = get_sample_data()
        return primary_metrics, quarterly_data, monthly_data, None
    except Exception as e:
        error_msg = f"Error loading data: {str(e)}"
        print(error_msg)
        return {
            'extraction_accuracy': 0.0,
            'document_accuracy': 0.0,
            'all_fields_accuracy': 0.0
        }, None, None, error_msg

primary_metrics, quarterly_data, monthly_data, data_error = load_dashboard_data()

def create_dashboard_layout():
    try:
        kpi_section = create_primary_kpi_section(primary_metrics)
        gauge_charts = create_primary_gauges_section(primary_metrics)
        monthly_carousel = create_monthly_carousel(
            monthly_data=monthly_data,
            selected_quarter="Q1-2025"
        )
        
        return create_responsive_layout(
            primary_metrics=primary_metrics,
            kpi_section=kpi_section,
            gauge_charts=gauge_charts,
            monthly_carousel=monthly_carousel
        )
    except Exception as e:
        print(f"Error creating dashboard layout: {e}")
        return html.Div([
            html.H1("Dashboard Error", className="text-center text-danger"),
            html.P(f"Error: {str(e)}", className="text-center"),
            html.P("Please check that all dependencies are installed.", className="text-center")
        ], className="container mt-5")

app.layout = create_dashboard_layout()


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
                --spacing-xs: 0.25rem;
                --spacing-sm: 0.5rem;
                --spacing-md: 0.75rem;
                --spacing-lg: 1rem;
                --spacing-xl: 1.5rem;
            }

            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background-color: var(--bg-secondary);
                background-image: radial-gradient(circle at 2px 2px, rgba(0,0,0,0.02) 1px, transparent 0);
                background-size: 20px 20px;
                color: var(--text-primary);
                font-size: 14px;
                line-height: 1.4;
            }
            
            .light-theme,
            .light-theme body,
            .dashboard-container.light-theme {
                background-color: var(--bg-secondary) !important;
                background-image: radial-gradient(circle at 2px 2px, rgba(0,0,0,0.02) 1px, transparent 0) !important;
                background-size: 20px 20px !important;
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
            
            .section-heading {
                font-size: 1.5rem;
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: var(--spacing-lg);
                line-height: 1.3;
                border-bottom: 2px solid var(--border-light);
                padding-bottom: var(--spacing-sm);
            }
            
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
            
            .btn:focus, .form-select:focus, .form-control:focus {
                box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
                outline: none;
            }
            
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