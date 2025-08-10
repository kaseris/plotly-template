"""
Tab Container component for organizing dashboard content.
"""

from dash import html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
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
        # Accuracy Overview tab - compact two-column layout
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
        
        # Create metrics dashboard sections grouped in cards
        custom_group_config = {
            "groups": [
                {"title": "Document Processing Overview", "cards_per_row": 2, "use_card_group": False},
                {"title": "Field Extraction Details", "cards_per_row": 4, "use_card_group": True}
            ]
        }
        
        # Prepare metrics dashboard card content
        metrics_dashboard = create_metrics_dashboard(group_config=custom_group_config)
        
        # Prepare KPI card content (only KPIs, no gauges)
        kpi_content = [
            html.H4("Extraction Accuracy", className="card-title mb-3", 
                   style={'fontWeight': '600', 'color': '#212529'}),
            kpi_section
        ]
        
        # Create the two-column layout
        content_sections = [
            # Two-column row with metrics and KPIs
            html.Section([
                dbc.Row([
                    # Left column - Document Metrics Dashboard (grouped in card)
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Document Extraction Metrics", 
                                       className="card-title mb-3",
                                       style={'fontWeight': '600', 'color': '#212529'}),
                                metrics_dashboard
                            ])
                        ], className="h-100")
                    ], width=12, md=6, className="mb-3"),
                    
                    # Right column - Extraction Accuracy KPIs only (grouped in card)
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(kpi_content)
                        ], className="h-100")
                    ], width=12, md=6, className="mb-3")
                ], className="g-3")
            ], className="mb-4", **{'aria-label': 'Dashboard Metrics Overview'})
        ]
        
        # Separate Gauge Charts Section (outside of cards)
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
                    html.H2("Quarterly Accuracy", className="section-heading mb-3 text-center"),
                    dbc.Row(gauge_row, className="g-2 justify-content-center")
                ], className="mb-4", **{'aria-label': 'Accuracy Gauge Charts'})
            )
        
        # Compact Monthly Carousel Section (full width below)
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


# Helper function for airline data
def get_airline_data():
    """Get the airline data for filtering."""
    return [
        {'Airline_Name': 'Aegean', 'Code': 'A3', 'Documents': 2, 'Accurate_Extraction': 1.00, 'Complete_Accurate_Extraction': 0.80, 'Flight_Number_Accuracy': 1.00, 'Flight_Origin_Accuracy': 0.80, 'Departure_Date_Accuracy': 0.80},
        {'Airline_Name': 'Aer Lingus', 'Code': 'EI', 'Documents': 5, 'Accurate_Extraction': 0.67, 'Complete_Accurate_Extraction': 0.67, 'Flight_Number_Accuracy': 1.00, 'Flight_Origin_Accuracy': 0.80, 'Departure_Date_Accuracy': 1.00},
        {'Airline_Name': 'Aeromexico', 'Code': 'AM', 'Documents': 1, 'Accurate_Extraction': 0.91, 'Complete_Accurate_Extraction': 1.00, 'Flight_Number_Accuracy': 0.91, 'Departure_Date_Accuracy': 0.92},
        {'Airline_Name': 'Air Canada', 'Code': 'AC', 'Documents': 23, 'Accurate_Extraction': 0.76, 'Complete_Accurate_Extraction': 0.48, 'Flight_Number_Accuracy': 1.00, 'Flight_Origin_Accuracy': 0.68, 'Departure_Date_Accuracy': 1.00},
        {'Airline_Name': 'Air China', 'Code': 'CA', 'Documents': 32, 'Accurate_Extraction': 0.94, 'Complete_Accurate_Extraction': 0.47, 'Flight_Number_Accuracy': 0.91, 'Flight_Origin_Accuracy': 0.68, 'Departure_Date_Accuracy': 0.90},
        {'Airline_Name': 'Air Europa', 'Code': 'UX', 'Documents': 1, 'Accurate_Extraction': 1.00, 'Complete_Accurate_Extraction': 1.00, 'Flight_Number_Accuracy': 1.00, 'Flight_Origin_Accuracy': 1.00, 'Departure_Date_Accuracy': 0.92},
        {'Airline_Name': 'Air France', 'Code': 'AF', 'Documents': 28, 'Accurate_Extraction': 0.82, 'Complete_Accurate_Extraction': 0.56, 'Flight_Number_Accuracy': 0.78, 'Flight_Origin_Accuracy': 1.00, 'Departure_Date_Accuracy': 0.90},
        {'Airline_Name': 'Air India', 'Code': 'AI', 'Documents': 9, 'Accurate_Extraction': 0.76, 'Complete_Accurate_Extraction': 0.79, 'Flight_Number_Accuracy': 0.93, 'Flight_Origin_Accuracy': 1.00, 'Departure_Date_Accuracy': 1.00},
        {'Airline_Name': 'Air New Zealand', 'Code': 'NZ', 'Documents': 11, 'Accurate_Extraction': 0.92, 'Complete_Accurate_Extraction': 0.56, 'Flight_Number_Accuracy': 0.78, 'Flight_Origin_Accuracy': 1.00, 'Departure_Date_Accuracy': 0.81},
        {'Airline_Name': 'Air Vanuatu', 'Code': 'VY', 'Documents': 1, 'Accurate_Extraction': 0.00, 'Complete_Accurate_Extraction': 0.92, 'Flight_Number_Accuracy': 0.92, 'Flight_Origin_Accuracy': 0.98, 'Departure_Date_Accuracy': 1.00},
        {'Airline_Name': 'Air Serbia', 'Code': 'JU', 'Documents': 2, 'Accurate_Extraction': 1.00, 'Complete_Accurate_Extraction': 0.50, 'Flight_Number_Accuracy': 1.00, 'Flight_Origin_Accuracy': 0.60, 'Departure_Date_Accuracy': 1.00},
        {'Airline_Name': 'Air Transat', 'Code': 'TS', 'Documents': 1, 'Accurate_Extraction': 1.00, 'Complete_Accurate_Extraction': 1.00, 'Flight_Number_Accuracy': 1.60, 'Flight_Origin_Accuracy': 0.50, 'Departure_Date_Accuracy': 1.00},
        {'Airline_Name': 'AirAsia', 'Code': 'AK', 'Documents': 47, 'Accurate_Extraction': 0.79, 'Complete_Accurate_Extraction': 0.00, 'Flight_Number_Accuracy': 1.00, 'Flight_Origin_Accuracy': 1.60, 'Departure_Date_Accuracy': 1.00},
        {'Airline_Name': 'Alaska Airlines', 'Code': 'AS', 'Documents': 1, 'Accurate_Extraction': 0.57, 'Complete_Accurate_Extraction': 0.72, 'Flight_Number_Accuracy': 0.94, 'Flight_Origin_Accuracy': 1.00, 'Departure_Date_Accuracy': 0.94},
        {'Airline_Name': 'All Nippon Airways', 'Code': 'NH', 'Documents': 6, 'Accurate_Extraction': 0.67, 'Complete_Accurate_Extraction': 0.67, 'Flight_Number_Accuracy': 1.00, 'Flight_Origin_Accuracy': 1.00, 'Departure_Date_Accuracy': 0.88},
        {'Airline_Name': 'Alliance Airlines', 'Code': 'QQ', 'Documents': 2, 'Accurate_Extraction': 1.00, 'Complete_Accurate_Extraction': 1.00, 'Flight_Number_Accuracy': 1.00, 'Flight_Origin_Accuracy': 0.67, 'Departure_Date_Accuracy': 1.00},
        {'Airline_Name': 'American Airlines', 'Code': 'AA', 'Documents': 35, 'Accurate_Extraction': 0.77, 'Complete_Accurate_Extraction': 0.00, 'Flight_Number_Accuracy': 0.00, 'Flight_Origin_Accuracy': 1.60, 'Departure_Date_Accuracy': 1.00},
        {'Airline_Name': 'Asiana Airlines', 'Code': 'OZ', 'Documents': 1, 'Accurate_Extraction': 1.00, 'Complete_Accurate_Extraction': 0.37, 'Flight_Number_Accuracy': 0.91, 'Flight_Origin_Accuracy': 1.62, 'Departure_Date_Accuracy': 0.91},
        {'Airline_Name': 'Austrian Airlines', 'Code': 'OS', 'Documents': 1, 'Accurate_Extraction': 1.00, 'Complete_Accurate_Extraction': 1.00, 'Flight_Number_Accuracy': 1.00, 'Flight_Origin_Accuracy': 1.60, 'Departure_Date_Accuracy': 1.00},
        {'Airline_Name': 'Batik Air Malaysia', 'Code': 'OD', 'Documents': 70, 'Accurate_Extraction': 0.60, 'Complete_Accurate_Extraction': 1.00, 'Flight_Number_Accuracy': 0.91, 'Flight_Origin_Accuracy': 1.62, 'Departure_Date_Accuracy': 0.90},
        {'Airline_Name': 'British Airways', 'Code': 'BA', 'Documents': 29, 'Accurate_Extraction': 0.86, 'Complete_Accurate_Extraction': 0.83, 'Flight_Number_Accuracy': 0.86, 'Flight_Origin_Accuracy': 0.56, 'Departure_Date_Accuracy': 1.00}
    ]


# Callback for airline search functionality
@callback(
    Output("airline-table-container", "children"),
    Input("airline-search-input", "value")
)
def update_airline_table(search_value: str) -> dash_table.DataTable:
    """
    Update the airline table based on search input.
    
    Args:
        search_value: Search term entered by user
    
    Returns:
        Filtered DataTable component
    """
    # Get the full airline data
    airline_data = get_airline_data()
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(airline_data)
    
    # Filter based on search input - only search by airline name and code
    if search_value and search_value.strip():
        search_term = search_value.lower().strip()
        
        # Create a mask for filtering only by airline name and code
        mask = (
            df['Airline_Name'].str.lower().str.contains(search_term, na=False) |
            df['Code'].str.lower().str.contains(search_term, na=False)
        )
        
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    # Create and return the filtered table
    return dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[
            {'name': 'Airline Name', 'id': 'Airline_Name', 'type': 'text'},
            {'name': 'Code', 'id': 'Code', 'type': 'text'},
            {'name': 'Documents', 'id': 'Documents', 'type': 'numeric'},
            {'name': 'Accurate Extraction', 'id': 'Accurate_Extraction', 'type': 'numeric', 'format': {'specifier': '.2f'}},
            {'name': 'Complete Accurate', 'id': 'Complete_Accurate_Extraction', 'type': 'numeric', 'format': {'specifier': '.2f'}},
            {'name': 'Flight Number', 'id': 'Flight_Number_Accuracy', 'type': 'numeric', 'format': {'specifier': '.2f'}},
            {'name': 'Flight Origin', 'id': 'Flight_Origin_Accuracy', 'type': 'numeric', 'format': {'specifier': '.2f'}},
            {'name': 'Departure Date', 'id': 'Departure_Date_Accuracy', 'type': 'numeric', 'format': {'specifier': '.2f'}}
        ],
        page_size=10,
        page_action='native',
        sort_action='native',
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontFamily': 'Arial, sans-serif',
            'fontSize': '14px',
            'border': '1px solid #dee2e6'
        },
        style_header={
            'backgroundColor': '#f8f9fa',
            'fontWeight': 'bold',
            'border': '1px solid #dee2e6'
        },
        style_data={
            'backgroundColor': 'white',
            'border': '1px solid #dee2e6'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            }
        ]
    )