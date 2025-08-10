"""
Main dashboard layout with responsive design and accessibility features.
Implements the layout strategy outlined in the CLAUDE.md plan.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, Optional
import pandas as pd
from src.components.accessibility_toolbar import create_collapsible_accessibility_toolbar, create_skip_navigation, create_screen_reader_summary
from src.components.tab_container import create_tab_container
from src.utils.accessibility_helpers import create_semantic_section, create_live_region


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
        # Collapsible accessibility toolbar
        create_collapsible_accessibility_toolbar(),
        
        # Action buttons removed per user request
    ], id="navigation", role="navigation", **{"aria-label": "Dashboard navigation and accessibility controls"})


def create_main_content_area(
    kpi_section: html.Div = None,
    gauge_charts: Dict = None,
    monthly_carousel: Optional[object] = None,
    primary_metrics: Optional[Dict[str, float]] = None,
    monthly_data: Optional[object] = None
) -> html.Div:
    """
    Create main content area with tab-based navigation.
    
    Args:
        kpi_section: KPI cards section (legacy, kept for compatibility)
        gauge_charts: Dictionary of gauge charts (legacy, kept for compatibility)
        monthly_carousel: Optional monthly carousel component (legacy, kept for compatibility)
        primary_metrics: Primary metrics data (legacy, kept for compatibility)
        monthly_data: Monthly data (legacy, kept for compatibility)
    
    Returns:
        Main content area HTML Div with tab container
    """
    # Tab configuration
    tab_config = [
        {
            'id': 'tab-1',
            'label': 'Accuracy Overview'
        },
        {
            'id': 'tab-2', 
            'label': 'Airline Analysis'
        },
        {
            'id': 'tab-3',
            'label': 'Field Analysis'
        }
    ]
    
    return html.Div([
        create_tab_container(tab_config, default_tab="tab-1")
    ])


# Removed: create_footer_section function - footer removed per user request


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
                
                # Footer removed per user request
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