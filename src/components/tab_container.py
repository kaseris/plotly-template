"""
Tab Container component for organizing dashboard content.
"""

from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
from typing import Dict, List, Optional, Any


def create_tab_container(
    tab_config: List[Dict[str, Any]], 
    default_tab: str = "tab-1"
) -> html.Div:
    """
    Create a dynamic tab container with configurable tabs.
    
    Args:
        tab_config: List of tab configurations with 'id', 'label', and 'content'
        default_tab: ID of the default active tab
    
    Returns:
        HTML Div containing tabs and content area
    """
    # Create tab components
    tabs = [
        dbc.Tab(
            label=config['label'],
            tab_id=config['id'],
            active_label_style={'color': '#0d6efd', 'fontWeight': '600'}
        )
        for config in tab_config
    ]
    
    return html.Div([
        dbc.Tabs(
            tabs,
            id="main-tabs",
            active_tab=default_tab,
            className="mb-4"
        ),
        html.Div(id="tab-content")
    ])


@callback(
    Output("tab-content", "children"),
    Input("main-tabs", "active_tab")
)
def render_tab_content(active_tab: str) -> html.Div:
    """
    Render content based on active tab.
    
    Args:
        active_tab: ID of the currently active tab
    
    Returns:
        Content for the active tab
    """
    if active_tab == "tab-1":
        # Accuracy Overview tab - using exact components from main branch
        from src.components.metrics_dashboard import create_metrics_dashboard
        from src.components.kpi_cards import create_primary_kpi_section
        from src.components.gauge_charts import create_primary_gauges_section
        from src.components.monthly_carousel import create_monthly_carousel
        from src.components.data_table import create_comprehensive_data_view
        from src.data.sample_data import get_sample_data
        from src.utils.performance_helpers import optimize_plotly_config
        from dash import dcc
        
        # Load real data exactly like in main branch
        try:
            primary_metrics, _, monthly_data = get_sample_data()
        except Exception:
            # Fallback to default data
            primary_metrics = {
                'extraction_accuracy': 0.0,
                'document_accuracy': 0.0,
                'all_fields_accuracy': 0.0
            }
            monthly_data = None
        
        # Create components exactly as in main branch
        kpi_section = create_primary_kpi_section(primary_metrics)
        gauge_charts = create_primary_gauges_section(primary_metrics)
        
        # Create monthly carousel with real data
        monthly_carousel = create_monthly_carousel(
            monthly_data=monthly_data if monthly_data is not None else None,
            selected_quarter="Q1-2025"
        )
        
        # Return exact structure from main branch layout
        content_sections = []
        
        # Metrics Dashboard Section with custom grouping
        custom_group_config = {
            "groups": [
                {"title": "Document Processing Overview", "cards_per_row": 2, "use_card_group": False},
                {"title": "Field Extraction Details", "cards_per_row": 4, "use_card_group": True}
            ]
        }
        
        content_sections.append(
            html.Section([
                create_metrics_dashboard(group_config=custom_group_config)
            ], className="mb-4", **{'aria-label': 'Document Metrics Dashboard'})
        )
        
        # Compact KPI Section
        content_sections.append(
            html.Section([
                html.H2("Extraction Accuracy", className="section-heading mb-3"),
                html.Div(kpi_section, id="overview")
            ], className="mb-4", **{'aria-label': 'Key Performance Indicators'})
        )
        
        # Compact Gauge Charts Section
        if gauge_charts:
            gauge_row = []
            for chart_name, chart_fig in gauge_charts.items():
                gauge_row.append(
                    dbc.Col([
                        dcc.Graph(
                            figure=chart_fig,
                            config=optimize_plotly_config(),
                            className="gauge-chart",
                            id=f"gauge-{chart_name}"
                        )
                    ], width=12, md=6, lg=4, className="mb-2")
                )
            
            content_sections.append(
                html.Section([
                    html.H2("Accuracy Gauges", className="section-heading mb-3 text-center"),
                    dbc.Row(gauge_row, className="g-2 justify-content-center")
                ], className="mb-4", **{'aria-label': 'Accuracy Gauge Charts'})
            )
        
        # Compact Monthly Carousel Section
        if monthly_carousel:
            content_sections.append(
                html.Section([
                    html.H2("Monthly Performance Overview", className="section-heading mb-3"),
                    html.Div(monthly_carousel, id="monthly-carousel-section")
                ], className="mb-4", **{'aria-label': 'Monthly Performance Carousel'})
            )
        
        # Compact Data Tables Section for Accessibility
        if primary_metrics:
            content_sections.append(
                html.Section([
                    create_comprehensive_data_view(
                        primary_metrics=primary_metrics,
                        monthly_data=monthly_data
                    )
                ], 
                id="data-tables-section",
                className="mb-3 screen-reader-enhanced", 
                **{'aria-label': 'Data tables for screen readers'})
            )
        
        return html.Div(content_sections)
        
    elif active_tab == "tab-2":
        # Airline Analysis tab
        from src.components.airline_analysis import create_airline_analysis_tab
        return create_airline_analysis_tab()
        
    elif active_tab == "tab-3":
        # Field Analysis tab
        from src.components.field_analysis import create_field_analysis_tab
        return create_field_analysis_tab()
        
    # Default fallback
    return html.Div([
        html.H3("Tab Content Not Found", className="text-center text-muted"),
        html.P("The selected tab content is not available.", className="text-center")
    ], className="p-5")