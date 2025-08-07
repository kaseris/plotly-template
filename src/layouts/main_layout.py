"""
Main dashboard layout with responsive design and accessibility features.
Implements the layout strategy outlined in the CLAUDE.md plan.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, Optional
import pandas as pd
from src.components.accessibility_toolbar import create_accessibility_toolbar, create_skip_navigation, create_screen_reader_summary
from src.components.data_table import create_comprehensive_data_view
from src.utils.accessibility_helpers import create_semantic_section, create_live_region
from src.utils.performance_helpers import optimize_plotly_config


def create_header_section(last_updated: Optional[str] = None) -> html.Div:
    """
    Create compact dashboard header with title and last updated timestamp.
    
    Args:
        last_updated: Last updated timestamp string
    
    Returns:
        Header section HTML Div
    """
    if last_updated is None:
        from datetime import datetime
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H1("Extraction Accuracy Dashboard", 
                       id="main-title",
                       className="text-center mb-1",
                       role="banner"),
                html.P(f"Last Updated: {last_updated}", 
                      className="text-center text-muted mb-2",
                      **{"aria-live": "polite"})
            ], width=12)
        ], className="g-0")
    ], className="mb-3")


def create_navigation_sidebar() -> dbc.Offcanvas:
    """
    Create collapsible navigation sidebar for mobile devices.
    
    Returns:
        Bootstrap Offcanvas component
    """
    nav_items = [
        {"label": "Overview", "href": "#overview", "icon": "📊"},
        {"label": "Monthly Carousel", "href": "#monthly-carousel-section", "icon": "📅"},
        {"label": "Export Data", "href": "#export", "icon": "💾"},
        {"label": "Help", "href": "#help", "icon": "❓"}
    ]
    
    sidebar_content = [
        html.H5("Navigation", className="mb-3"),
        html.Hr(),
    ]
    
    for item in nav_items:
        sidebar_content.append(
            dbc.Button([
                html.Span(item["icon"], className="me-2"),
                item["label"]
            ],
            href=item["href"],
            color="light",
            className="mb-2 w-100 text-start",
            outline=True
            )
        )
    
    return dbc.Offcanvas(
        sidebar_content,
        id="offcanvas-sidebar",
        title="Dashboard Navigation",
        is_open=False,
        placement="start",
        style={'width': '280px'}
    )


def create_control_panel() -> html.Div:
    """
    Create compact control panel with filters and actions.
    
    Returns:
        Control panel HTML Div
    """
    return html.Div([
        # Accessibility toolbar
        create_accessibility_toolbar(),
        
        # Compact main controls
        dbc.Card([
            dbc.CardBody([
                html.H6("Dashboard Controls", className="card-title mb-2", id="controls-heading"),
                dbc.Row([
                    dbc.Col([
                        html.Label("View Mode:", className="form-label", htmlFor="view-mode-dropdown"),
                        dcc.Dropdown(
                            id='view-mode-dropdown',
                            options=[
                                {'label': 'Overview', 'value': 'overview'},
                                {'label': 'Detailed', 'value': 'detailed'},
                                {'label': 'Comparison', 'value': 'comparison'}
                            ],
                            value='overview',
                            className="mb-1"
                        )
                    ], width=12, md=4),
                    dbc.Col([
                        html.Label("Time Range:", className="form-label", htmlFor="time-range-dropdown"),
                        dcc.Dropdown(
                            id='time-range-dropdown',
                            options=[
                                {'label': '6 Months', 'value': '6m'},
                                {'label': '1 Year', 'value': '1y'},
                                {'label': '2 Years', 'value': '2y'},
                                {'label': 'All Time', 'value': 'all'}
                            ],
                            value='1y',
                            className="mb-1"
                        )
                    ], width=12, md=4),
                    dbc.Col([
                        html.Label("Actions:", className="form-label"),
                        dbc.ButtonGroup([
                            dbc.Button("Refresh", 
                                     id="refresh-btn", 
                                     color="primary", 
                                     size="sm",
                                     title="Refresh dashboard data"),
                            dbc.Button("Export", 
                                     id="export-btn", 
                                     color="secondary", 
                                     size="sm",
                                     title="Export data as CSV file"),
                            dbc.Button("☰", 
                                     id="sidebar-toggle", 
                                     color="light", 
                                     size="sm",
                                     title="Toggle sidebar")
                        ], className="w-100 d-grid")
                    ], width=12, md=4)
                ], className="g-2")
            ], className="py-2")
        ], className="mb-3")
    ], id="navigation", role="navigation", **{"aria-label": "Dashboard controls and navigation"})


def create_main_content_area(
    kpi_section: html.Div,
    gauge_charts: Dict,
    monthly_carousel: Optional[object] = None,
    primary_metrics: Optional[Dict[str, float]] = None,
    monthly_data: Optional[object] = None
) -> html.Div:
    """
    Create compact main content area with responsive grid layout.
    
    Args:
        kpi_section: KPI cards section
        gauge_charts: Dictionary of gauge charts
        monthly_carousel: Optional monthly carousel component
    
    Returns:
        Main content area HTML Div
    """
    content_sections = []
    
    # Compact KPI Section
    content_sections.append(
        html.Section([
            html.Div(kpi_section, id="overview")
        ], className="mb-3", **{'aria-label': 'Key Performance Indicators'})
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
                html.H3("Accuracy Gauges", className="mb-2 text-center h5"),
                dbc.Row(gauge_row, className="g-2 justify-content-center")
            ], className="mb-3", **{'aria-label': 'Accuracy Gauge Charts'})
        )
    
    # Compact Monthly Carousel Section
    if monthly_carousel:
        content_sections.append(
            html.Section([
                html.Div(monthly_carousel, id="monthly-carousel-section")
            ], className="mb-3", **{'aria-label': 'Monthly Performance Carousel'})
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


def create_footer_section() -> html.Div:
    """
    Create compact dashboard footer with accessibility and help information.
    
    Returns:
        Footer section HTML Div
    """
    return html.Footer([
        html.Hr(className="my-2"),
        dbc.Row([
            dbc.Col([
                html.P([
                    "Built with ",
                    html.A("Plotly Dash", href="https://dash.plotly.com/", target="_blank", className="text-decoration-none"),
                    " • ",
                    html.A("Accessibility", href="#help", id="accessibility-link", className="text-decoration-none"),
                    " • ",
                    html.A("Shortcuts", href="#help", id="shortcuts-link", className="text-decoration-none")
                ], className="text-muted small mb-0")
            ], width=12, className="text-center")
        ], className="g-0")
    ], className="mt-3 py-2")


def create_responsive_layout(
    primary_metrics: Dict[str, float],
    kpi_section: html.Div,
    gauge_charts: Dict,
    monthly_carousel: Optional[object] = None
) -> html.Div:
    """
    Create the complete responsive dashboard layout.
    
    Args:
        primary_metrics: Primary KPI metrics
        kpi_section: KPI cards section component
        gauge_charts: Dictionary of gauge chart figures
        monthly_carousel: Optional monthly carousel component
    
    Returns:
        Complete dashboard layout
    """
    return html.Div([
        # Skip navigation links
        create_skip_navigation(),
        
        # Store components for callbacks
        dcc.Store(id='metrics-store', data=primary_metrics),
        dcc.Store(id='view-state', data={'current_view': 'overview'}),
        
        # Screen reader summary
        create_screen_reader_summary(primary_metrics),
        
        # Live regions for dynamic updates
        create_live_region('status-updates'),
        create_live_region('error-messages', 'assertive'),
        
        # Navigation sidebar
        create_navigation_sidebar(),
        
        # Main container
        html.Main([
            dbc.Container([
                # Header section
                create_header_section(),
                
                # Control panel
                create_control_panel(),
                
                # Main content
                create_main_content_area(
                    kpi_section=kpi_section,
                    gauge_charts=gauge_charts,
                    monthly_carousel=monthly_carousel,
                    primary_metrics=primary_metrics
                ),
                
                # Footer
                create_footer_section()
            ], fluid=True, className="px-3 px-md-4")
        ], id="main-content", role="main", **{"aria-label": "Main dashboard content"}),
        
        # Loading overlay
        dcc.Loading(
            id="loading-overlay",
            type="dot",
            children=html.Div(
                id="loading-output",
                **{"aria-live": "polite", "aria-label": "Loading dashboard content"}
            ),
            style={'position': 'fixed', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)'}
        )
    ], id="dashboard-container", className="dashboard-container light-theme", lang="en")


def get_responsive_breakpoints() -> Dict[str, str]:
    """
    Get CSS breakpoints for responsive design.
    
    Returns:
        Dictionary of breakpoint definitions
    """
    return {
        'mobile': '(max-width: 767px)',
        'tablet': '(min-width: 768px) and (max-width: 1199px)',
        'desktop': '(min-width: 1200px)'
    }