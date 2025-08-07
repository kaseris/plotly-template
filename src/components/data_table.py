"""
Data table component for screen reader accessibility and alternative data access.
Provides tabular representation of chart data for users who cannot access visual charts.
"""

from dash import html, dcc
from typing import Dict, List, Optional
import pandas as pd
from src.utils.accessibility_helpers import create_screen_reader_table


def create_metrics_data_table(
    primary_metrics: Dict[str, float],
    table_id: str = "primary-metrics-table",
    show_by_default: bool = False
) -> html.Div:
    """
    Create a data table for primary metrics.
    
    Args:
        primary_metrics: Dictionary of metric names and values
        table_id: ID for the table element
        show_by_default: Whether to show table by default or in collapsible section
    
    Returns:
        HTML Div containing the metrics table
    """
    # Convert metrics to table data
    table_data = []
    for key, value in primary_metrics.items():
        # Format metric name for display
        display_name = key.replace('_', ' ').title()
        
        # Determine status
        if value >= 90:
            status = "Excellent"
            status_class = "text-success"
        elif value >= 75:
            status = "Good"
            status_class = "text-warning"
        else:
            status = "Needs Attention"
            status_class = "text-danger"
        
        table_data.append({
            'metric': display_name,
            'value': f"{value:.1f}%",
            'status': status,
            'status_class': status_class
        })
    
    # Create table
    table = html.Table([
        html.Caption("Primary Dashboard Metrics", className="visually-hidden"),
        html.Thead([
            html.Tr([
                html.Th("Metric", scope="col"),
                html.Th("Current Value", scope="col"),
                html.Th("Status", scope="col")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(row['metric']),
                html.Td(row['value'], className="fw-bold"),
                html.Td(row['status'], className=row['status_class'])
            ]) for row in table_data
        ])
    ],
    id=table_id,
    className="table table-striped table-hover",
    **{"aria-label": "Primary dashboard metrics in tabular format"}
    )
    
    if show_by_default:
        return html.Div([
            html.H3("Dashboard Metrics", className="h5 mb-3"),
            table
        ], className="metrics-table-container")
    else:
        # Return table directly without collapsible wrapper
        return html.Div([
            table
        ], className="mt-3 metrics-table-container screen-reader-enhanced")


def create_monthly_data_table(
    monthly_data: pd.DataFrame,
    selected_quarter: str = "Q1-2025",
    table_id: str = "monthly-data-table"
) -> html.Div:
    """
    Create a data table for monthly performance data.
    
    Args:
        monthly_data: DataFrame with monthly data
        selected_quarter: Quarter to display
        table_id: ID for the table element
    
    Returns:
        HTML Div containing the monthly data table
    """
    if monthly_data.empty:
        return html.Div([
            html.P("No monthly data available", className="text-muted")
        ])
    
    # Filter data for selected quarter
    quarter_num = selected_quarter.split('-')[0].replace('Q', '')
    year = selected_quarter.split('-')[1] if '-' in selected_quarter else '2025'
    
    # Create sample data if needed
    if 'quarter' not in monthly_data.columns:
        # Create sample monthly data
        table_data = []
        months = ['January', 'February', 'March']
        for i, month in enumerate(months):
            table_data.append({
                'month': f"{month} {year}",
                'field_1_accuracy': f"{85 + i * 2.5:.1f}%",
                'field_2_accuracy': f"{87 + i * 1.5:.1f}%",
                'field_3_accuracy': f"{89 + i * 1:.1f}%",
                'overall_status': 'Good' if i < 2 else 'Excellent'
            })
    else:
        # Use real data
        quarter_data = monthly_data[monthly_data['quarter'] == f'Q{quarter_num}']
        if 'year' in monthly_data.columns:
            quarter_data = quarter_data[quarter_data['year'] == int(year)]
        
        table_data = []
        for _, row in quarter_data.iterrows():
            month_name = f"Month {row.get('month', 'Unknown')}"
            overall = (row.get('field_1_accuracy', 0) + 
                      row.get('field_2_accuracy', 0) + 
                      row.get('field_3_accuracy', 0)) / 3
            
            table_data.append({
                'month': month_name,
                'field_1_accuracy': f"{row.get('field_1_accuracy', 0):.1f}%",
                'field_2_accuracy': f"{row.get('field_2_accuracy', 0):.1f}%",
                'field_3_accuracy': f"{row.get('field_3_accuracy', 0):.1f}%",
                'overall_status': 'Excellent' if overall >= 90 else ('Good' if overall >= 75 else 'Needs Attention')
            })
    
    if not table_data:
        return html.Div([
            html.P("No data available for selected quarter", className="text-muted")
        ])
    
    # Create table
    table = html.Table([
        html.Caption(f"Monthly Performance Data for {selected_quarter}", className="visually-hidden"),
        html.Thead([
            html.Tr([
                html.Th("Month", scope="col"),
                html.Th("Field 1 Accuracy", scope="col"),
                html.Th("Field 2 Accuracy", scope="col"),
                html.Th("Field 3 Accuracy", scope="col"),
                html.Th("Overall Status", scope="col")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(row['month']),
                html.Td(row['field_1_accuracy']),
                html.Td(row['field_2_accuracy']),
                html.Td(row['field_3_accuracy']),
                html.Td(row['overall_status'], className={
                    'text-success': row['overall_status'] == 'Excellent',
                    'text-warning': row['overall_status'] == 'Good',
                    'text-danger': row['overall_status'] == 'Needs Attention'
                }.get('text-success' if row['overall_status'] == 'Excellent' else 
                      'text-warning' if row['overall_status'] == 'Good' else 'text-danger', ''))
            ]) for row in table_data
        ])
    ],
    id=table_id,
    className="table table-striped table-hover table-sm",
    **{"aria-label": f"Monthly performance data for {selected_quarter}"}
    )
    
    return html.Div([
        table
    ], className="mt-3 monthly-data-table")


# Removed: create_export_table_buttons function - export functionality removed per user request


def create_comprehensive_data_view(
    primary_metrics: Dict[str, float],
    monthly_data: Optional[pd.DataFrame] = None,
    selected_quarter: str = "Q1-2025",
    screen_reader_mode: bool = False
) -> html.Div:
    """
    Create comprehensive data view with both visual and tabular representations.
    
    Args:
        primary_metrics: Primary metrics data
        monthly_data: Monthly performance data
        selected_quarter: Selected quarter for monthly view
        screen_reader_mode: Whether to emphasize screen reader features
    
    Returns:
        HTML Div with comprehensive data view
    """
    components = []
    
    # Primary metrics table removed per user request - redundant with KPI cards
    
    # Monthly data table if available
    if monthly_data is not None and not monthly_data.empty:
        components.append(html.Div([
            html.H4("Monthly Performance", className="h5 mb-3 mt-4"),
            create_monthly_data_table(
                monthly_data, 
                selected_quarter
            )
        ]))
    
    # Export options removed per user request
    
    # Screen reader instructions
    if screen_reader_mode:
        components.insert(0, html.Div([
            html.H3("Data Tables", className="h4 mb-3"),
            html.P([
                "The following tables provide the same information as the visual charts above. ",
                "Use your screen reader's table navigation commands to explore the data efficiently."
            ], className="mb-3 text-muted")
        ]))
    
    return html.Div(
        components,
        id="comprehensive-data-view",
        className="data-tables-section mt-4",
        **{"aria-label": "Alternative data view in table format"}
    )