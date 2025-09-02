"""
PDF Export Button Component for the dashboard.
Provides UI and callback functionality for screenshot-based PDF export.
"""

from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
from datetime import datetime
import asyncio
import base64
from typing import Dict, Optional, Any

from src.utils.screenshot_pdf_export import screenshot_pdf_exporter


def create_pdf_export_button() -> html.Div:
    """
    Create PDF export button component with download functionality.
    
    Returns:
        HTML Div containing the export button and download component
    """
    return html.Div([
        dbc.Button([
            html.I(className="fas fa-file-pdf me-2"),
            "Export PDF"
        ],
        id="pdf-export-btn",
        color="primary",
        size="sm",
        className="me-2",
        title="Export dashboard as PDF"
        ),
        
        dcc.Download(id="pdf-download"),
        
        # Loading indicator for export process
        html.Div([
            dbc.Spinner(
                html.Div(id="pdf-export-status"),
                id="pdf-export-spinner",
                size="sm",
                color="primary"
            )
        ], id="pdf-export-spinner-container", className="d-none")
    ], className="d-inline-flex align-items-center")


@callback(
    Output("pdf-download", "data"),
    Output("pdf-export-status", "children"),
    Output("pdf-export-spinner-container", "className"),
    Input("pdf-export-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_pdf_export(n_clicks: int) -> tuple:
    """
    Handle PDF export when button is clicked.
    Uses screenshot-based approach to capture actual dashboard content.
    
    Args:
        n_clicks: Number of button clicks
        
    Returns:
        Tuple of (download_data, status_message, spinner_class)
    """
    if not n_clicks:
        return None, "", "d-none"
    
    try:
        # Show loading spinner
        spinner_class = ""
        
        # Run async screenshot export
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            pdf_bytes = loop.run_until_complete(
                screenshot_pdf_exporter.export_dashboard_to_pdf(
                    base_url="http://localhost:8050",
                    title="Dashboard Screenshots Export"
                )
            )
        finally:
            loop.close()
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dashboard_screenshots_{timestamp}.pdf"
        
        # Prepare download data
        download_data = {
            "content": base64.b64encode(pdf_bytes).decode(),
            "filename": filename,
            "base64": True,
            "type": "application/pdf"
        }
        
        return download_data, "PDF exported successfully!", "d-none"
        
    except Exception as e:
        error_message = f"Export failed: {str(e)}"
        print(error_message)
        return None, error_message, "d-none"




def create_export_options_modal() -> dbc.Modal:
    """
    Create modal dialog for export options (future enhancement).
    
    Returns:
        Bootstrap Modal component for export options
    """
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Export Options")),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Include Sections:"),
                    dbc.Checklist(
                        id="export-sections",
                        options=[
                            {"label": "KPI Summary", "value": "kpis", "disabled": False},
                            {"label": "Gauge Charts", "value": "gauges", "disabled": False},
                            {"label": "Monthly Data", "value": "monthly", "disabled": False},
                            {"label": "Airline Analysis", "value": "airline", "disabled": False},
                            {"label": "Field Analysis", "value": "fields", "disabled": False},
                        ],
                        value=["kpis", "gauges", "monthly", "airline", "fields"],
                        inline=False
                    )
                ], width=6),
                dbc.Col([
                    dbc.Label("Page Layout:"),
                    dbc.RadioItems(
                        id="export-layout",
                        options=[
                            {"label": "Portrait", "value": "portrait"},
                            {"label": "Landscape", "value": "landscape"},
                        ],
                        value="portrait",
                        inline=True
                    ),
                    html.Hr(),
                    dbc.Label("Chart Size:"),
                    dbc.RadioItems(
                        id="export-chart-size",
                        options=[
                            {"label": "Standard", "value": "standard"},
                            {"label": "Large", "value": "large"},
                        ],
                        value="standard",
                        inline=True
                    )
                ], width=6)
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancel", id="export-cancel", className="me-1", color="secondary"),
            dbc.Button("Export PDF", id="export-confirm", color="primary")
        ])
    ], id="export-options-modal", is_open=False)


# Enhanced export button with options (for future use)
def create_advanced_pdf_export_button() -> html.Div:
    """
    Create advanced PDF export button with options modal.
    
    Returns:
        HTML Div containing export button with options
    """
    return html.Div([
        dbc.ButtonGroup([
            dbc.Button([
                html.I(className="fas fa-file-pdf me-2"),
                "Export PDF"
            ],
            id="pdf-export-btn-advanced",
            color="primary",
            size="sm"
            ),
            dbc.DropdownMenu([
                dbc.DropdownMenuItem("Quick Export", id="quick-export"),
                dbc.DropdownMenuItem("Export Options...", id="export-options"),
            ],
            toggle_style={"border-left": "1px solid rgba(255,255,255,0.3)"},
            direction="down",
            color="primary",
            size="sm"
            )
        ]),
        
        create_export_options_modal(),
        dcc.Download(id="pdf-download-advanced"),
        
        html.Div([
            dbc.Spinner(
                html.Div(id="pdf-export-status-advanced"),
                id="pdf-export-spinner-advanced",
                size="sm",
                color="primary"
            )
        ], className="d-none ms-2")
    ], className="d-inline-flex align-items-center")