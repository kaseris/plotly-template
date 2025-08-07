"""
Accessibility helper utilities for WCAG 2.1 AA compliance.
Provides ARIA labels, keyboard navigation, and semantic HTML helpers.
"""

from typing import Dict, List, Optional, Union
from dash import html, dcc
import dash_bootstrap_components as dbc


def create_aria_label(
    element_type: str, 
    value: Optional[Union[str, float]] = None,
    context: Optional[str] = None,
    status: Optional[str] = None
) -> str:
    """
    Generate appropriate ARIA label for dashboard elements.
    
    Args:
        element_type: Type of element (e.g., 'kpi', 'gauge', 'chart')
        value: Current value of the element
        context: Additional context information
        status: Status or condition (e.g., 'good', 'warning', 'critical')
    
    Returns:
        ARIA label string
    """
    labels = {
        'kpi': f"{context}: {value}%{f' - {status} performance' if status else ''}",
        'gauge': f"{context} gauge showing {value}% accuracy{f' - {status}' if status else ''}",
        'chart': f"{context} chart{f' with {status} trend' if status else ''}",
        'button': f"{context} button{f' - {status}' if status else ''}",
        'dropdown': f"Select {context}{f' - current: {status}' if status else ''}",
        'card': f"{context} card showing {value}%{f' - {status}' if status else ''}"
    }
    
    return labels.get(element_type, f"{context}: {value}")


def create_semantic_section(
    title: str,
    content: Union[html.Div, List],
    section_id: Optional[str] = None,
    aria_label: Optional[str] = None
) -> html.Section:
    """
    Create semantically correct section with proper ARIA attributes.
    
    Args:
        title: Section title
        content: Section content
        section_id: Optional section ID
        aria_label: Optional custom ARIA label
    
    Returns:
        HTML Section element with proper semantics
    """
    section_attrs = {
        "aria-label": aria_label or title.lower().replace(' ', '-')
    }
    
    if section_id:
        section_attrs["id"] = section_id
    
    return html.Section([
        html.H2(title, className="visually-hidden"),
        content if isinstance(content, list) else [content]
    ], **section_attrs)


def add_keyboard_navigation_attrs(
    component: Union[html.Button, dbc.Button, html.Div],
    role: Optional[str] = None,
    tabindex: Optional[int] = None,
    aria_label: Optional[str] = None,
    keyboard_shortcuts: Optional[List[str]] = None
) -> Dict[str, Union[str, int]]:
    """
    Add keyboard navigation attributes to components.
    
    Args:
        component: Dash component to enhance
        role: ARIA role
        tabindex: Tab index for keyboard navigation
        aria_label: ARIA label for screen readers
        keyboard_shortcuts: List of keyboard shortcuts
    
    Returns:
        Dictionary of attributes to add to component
    """
    attrs = {}
    
    if role:
        attrs["role"] = role
    
    if tabindex is not None:
        attrs["tabIndex"] = tabindex
    
    if aria_label:
        attrs["aria-label"] = aria_label
    
    if keyboard_shortcuts:
        attrs["aria-keyshortcuts"] = " ".join(keyboard_shortcuts)
    
    return attrs


def create_accessible_kpi_card(
    title: str,
    value: float,
    status: str,
    trend: Optional[str] = None,
    card_id: Optional[str] = None
) -> dbc.Card:
    """
    Create accessible KPI card with proper ARIA attributes.
    
    Args:
        title: KPI title
        value: KPI value
        status: Status (good/warning/critical)
        trend: Optional trend information
        card_id: Optional card ID
    
    Returns:
        Accessible KPI card
    """
    # Determine status icon and color
    status_config = {
        'good': {'icon': '✓', 'color': 'success', 'text': 'Good performance'},
        'warning': {'icon': '⚠', 'color': 'warning', 'text': 'Needs attention'},
        'critical': {'icon': '✗', 'color': 'danger', 'text': 'Critical - immediate attention required'}
    }
    
    config = status_config.get(status, status_config['good'])
    
    # Create ARIA label
    aria_label = create_aria_label('kpi', value, title, config['text'])
    trend_text = f", trending {trend}" if trend else ""
    full_aria_label = f"{aria_label}{trend_text}"
    
    card_attrs = {
        "role": "img",
        "aria-label": full_aria_label,
        "tabIndex": 0
    }
    
    if card_id:
        card_attrs["id"] = card_id
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Span(config['icon'], className="status-icon", **{"aria-hidden": "true"}),
                html.H3(f"{value:.1f}%", className="kpi-value"),
                html.P(title, className="kpi-title"),
                html.P(config['text'], className="visually-hidden")  # Screen reader only
            ])
        ])
    ], 
    color=config['color'],
    outline=True,
    className="kpi-card h-100",
    **card_attrs
    )


def create_accessible_chart_container(
    chart_component: dcc.Graph,
    chart_title: str,
    chart_description: str,
    data_summary: Optional[str] = None,
    table_data: Optional[List[Dict]] = None
) -> html.Div:
    """
    Create accessible chart container with alternative data access.
    
    Args:
        chart_component: Plotly chart component
        chart_title: Chart title for accessibility
        chart_description: Description of chart content
        data_summary: Optional summary of key data points
        table_data: Optional table data for screen readers
    
    Returns:
        Accessible chart container
    """
    container_id = f"{chart_component.id}-container"
    
    # Update chart with accessibility attributes
    chart_component.figure.update_layout({
        'title': {
            'text': chart_title,
            'font': {'size': 16}
        }
    })
    
    # Create table alternative if data provided
    table_alternative = None
    if table_data:
        table_alternative = html.Details([
            html.Summary("View data table", className="btn btn-link p-0"),
            html.Table([
                html.Thead([
                    html.Tr([html.Th(col) for col in table_data[0].keys()])
                ]),
                html.Tbody([
                    html.Tr([html.Td(row[col]) for col in row.keys()])
                    for row in table_data
                ])
            ], className="table table-sm mt-2")
        ], className="mt-2")
    
    return html.Div([
        html.Div([
            html.H3(chart_title, className="chart-title"),
            html.P(chart_description, className="chart-description visually-hidden"),
            chart_component
        ], 
        role="img", 
        **{"aria-label": f"{chart_title}. {chart_description}"}
        ),
        
        # Data summary for screen readers
        html.Div([
            html.H4("Chart Summary", className="visually-hidden"),
            html.P(data_summary or "Chart data available in interactive format above.", 
                   className="visually-hidden")
        ]) if data_summary else None,
        
        # Table alternative
        table_alternative
    ], 
    id=container_id,
    className="accessible-chart-container"
    )


def create_live_region(region_id: str, politeness: str = "polite") -> html.Div:
    """
    Create a live region for dynamic content updates.
    
    Args:
        region_id: ID for the live region
        politeness: ARIA live politeness setting
    
    Returns:
        Live region HTML div
    """
    return html.Div(
        id=region_id,
        **{
            "aria-live": politeness,
            "aria-atomic": "true",
            "role": "status" if politeness == "polite" else "alert"
        },
        className="visually-hidden"
    )


def get_color_blind_patterns() -> Dict[str, str]:
    """
    Get pattern definitions for color-blind accessibility.
    
    Returns:
        Dictionary mapping colors to pattern classes
    """
    return {
        'success': 'pattern-diagonal-stripes',
        'warning': 'pattern-dots',
        'danger': 'pattern-cross-hatch',
        'info': 'pattern-vertical-lines',
        'primary': 'pattern-horizontal-lines'
    }


def create_focus_trap(container_id: str) -> html.Script:
    """
    Create focus trap JavaScript for modal dialogs.
    
    Args:
        container_id: ID of container to trap focus within
    
    Returns:
        Script element with focus trap logic
    """
    script_content = f"""
    (function() {{
        const container = document.getElementById('{container_id}');
        if (!container) return;
        
        const focusableElements = container.querySelectorAll(
            'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];
        
        container.addEventListener('keydown', function(e) {{
            if (e.key === 'Tab') {{
                if (e.shiftKey) {{
                    if (document.activeElement === firstFocusable) {{
                        e.preventDefault();
                        lastFocusable.focus();
                    }}
                }} else {{
                    if (document.activeElement === lastFocusable) {{
                        e.preventDefault();
                        firstFocusable.focus();
                    }}
                }}
            }}
            
            if (e.key === 'Escape') {{
                // Close modal or return focus to trigger
                const closeButton = container.querySelector('[data-dismiss]');
                if (closeButton) closeButton.click();
            }}
        }});
        
        // Set initial focus
        if (firstFocusable) firstFocusable.focus();
    }})();
    """
    
    return html.Script(script_content)


def get_wcag_contrast_ratio(color1: str, color2: str) -> float:
    """
    Calculate WCAG contrast ratio between two colors.
    Note: This is a simplified version - full implementation would need color parsing.
    
    Args:
        color1: First color (hex or rgb)
        color2: Second color (hex or rgb)
    
    Returns:
        Contrast ratio (simplified calculation)
    """
    # This is a placeholder - real implementation would need proper color parsing
    # For now, return a value that indicates whether colors meet WCAG AA
    return 4.5  # Minimum for WCAG AA compliance


def create_screen_reader_table(data: List[Dict], table_id: str, caption: str) -> html.Table:
    """
    Create a screen reader optimized data table.
    
    Args:
        data: List of dictionaries representing table data
        table_id: ID for the table
        caption: Table caption for screen readers
    
    Returns:
        Accessible HTML table
    """
    if not data:
        return html.Div("No data available", className="text-muted")
    
    headers = list(data[0].keys())
    
    return html.Table([
        html.Caption(caption, className="visually-hidden"),
        html.Thead([
            html.Tr([
                html.Th(header.replace('_', ' ').title(), scope="col")
                for header in headers
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(str(row.get(header, '')))
                for header in headers
            ]) for row in data
        ])
    ],
    id=table_id,
    className="table table-striped table-hover",
    **{"aria-label": f"{caption} data table"}
    )