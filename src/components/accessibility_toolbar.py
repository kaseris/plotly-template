"""
Accessibility Toolbar component for dashboard accessibility controls.
Provides theme toggle, text size adjustment, and screen reader mode options.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Optional


def create_accessibility_toolbar(
    high_contrast_mode: bool = False,
    text_size: str = "normal",
    screen_reader_mode: bool = False
) -> html.Div:
    """
    Create accessibility toolbar with various accessibility controls.
    
    Args:
        high_contrast_mode: Whether high contrast mode is enabled
        text_size: Current text size setting ("small", "normal", "large")
        screen_reader_mode: Whether screen reader mode is enabled
    
    Returns:
        HTML Div containing accessibility controls
    """
    
    return html.Div([
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H6([
                        html.I(className="fas fa-universal-access me-2", **{"aria-hidden": "true"}),
                        "Accessibility Options"
                    ], className="card-title mb-3"),
                    
                    # Theme and contrast controls
                    html.Div([
                        html.Label("Display Mode:", className="form-label small fw-bold"),
                        dbc.ButtonGroup([
                            dbc.Button(
                                [html.I(className="fas fa-sun me-1"), "Normal"],
                                id="normal-theme-btn",
                                color="outline-secondary",
                                size="sm",
                                active=not high_contrast_mode,
                                title="Switch to normal theme"
                            ),
                            dbc.Button(
                                [html.I(className="fas fa-adjust me-1"), "High Contrast"],
                                id="high-contrast-btn",
                                color="outline-dark",
                                size="sm",
                                active=high_contrast_mode,
                                title="Switch to high contrast theme"
                            )
                        ], className="w-100 mb-3")
                    ]),
                    
                    # Text size controls
                    html.Div([
                        html.Label("Text Size:", className="form-label small fw-bold"),
                        dbc.ButtonGroup([
                            dbc.Button(
                                "A",
                                id="text-small-btn",
                                color="outline-secondary",
                                size="sm",
                                active=text_size == "small",
                                style={'fontSize': '0.8rem'},
                                title="Small text size"
                            ),
                            dbc.Button(
                                "A",
                                id="text-normal-btn",
                                color="outline-secondary",
                                size="sm",
                                active=text_size == "normal",
                                style={'fontSize': '1rem'},
                                title="Normal text size"
                            ),
                            dbc.Button(
                                "A",
                                id="text-large-btn",
                                color="outline-secondary",
                                size="sm",
                                active=text_size == "large",
                                style={'fontSize': '1.2rem'},
                                title="Large text size"
                            )
                        ], className="w-100 mb-3")
                    ]),
                    
                    # Additional accessibility features
                    html.Div([
                        html.Label("Additional Features:", className="form-label small fw-bold"),
                        dbc.Checklist([
                            {
                                "label": html.Span([
                                    html.I(className="fas fa-table me-2"),
                                    "Screen Reader Tables"
                                ]),
                                "value": "screen_reader_mode"
                            },
                            {
                                "label": html.Span([
                                    html.I(className="fas fa-palette me-2"),
                                    "Color-Blind Friendly"
                                ]),
                                "value": "colorblind_mode"
                            }
                        ],
                        id="accessibility-features",
                        value=["screen_reader_mode"] if screen_reader_mode else [],
                        className="mb-3"
                        )
                    ]),
                    
                    # Keyboard shortcuts info
                    html.Div([
                        dbc.Button(
                            [html.I(className="fas fa-keyboard me-2"), "Keyboard Shortcuts"],
                            id="keyboard-shortcuts-btn",
                            color="link",
                            size="sm",
                            className="p-0 text-decoration-none"
                        )
                    ])
                ])
            ])
        ], className="shadow-sm mb-3"),
        
        # Hidden stores for state management
        dcc.Store(id="accessibility-state", data={
            "high_contrast": high_contrast_mode,
            "text_size": text_size,
            "screen_reader_mode": screen_reader_mode,
            "colorblind_mode": False
        }),
        
        # Keyboard shortcuts modal
        dbc.Modal([
            dbc.ModalHeader("Keyboard Shortcuts", id="shortcuts-modal-header"),
            dbc.ModalBody([
                html.Div([
                    html.H6("Navigation:", className="fw-bold mb-2"),
                    html.Ul([
                        html.Li("Tab / Shift+Tab: Navigate through elements"),
                        html.Li("Enter / Space: Activate buttons and controls"),
                        html.Li("Escape: Close modals and menus"),
                        html.Li("Arrow keys: Navigate within components")
                    ], className="mb-3"),
                    
                    html.H6("Dashboard Actions:", className="fw-bold mb-2"),
                    html.Ul([
                        html.Li("R: Refresh dashboard data"),
                        html.Li("H: Toggle this help modal"),
                        html.Li("C: Toggle high contrast mode"),
                        html.Li("T: Cycle text size options")
                    ], className="mb-3"),
                    
                    html.H6("Charts:", className="fw-bold mb-2"),
                    html.Ul([
                        html.Li("Focus on chart, then use arrow keys to navigate data points"),
                        html.Li("Enter: Activate chart interactions"),
                        html.Li("Plus/Minus: Zoom in/out on focused charts")
                    ])
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button("Close", id="close-shortcuts-modal", color="secondary")
            ])
        ],
        id="keyboard-shortcuts-modal",
        is_open=False,
        size="lg"
        )
        
    ], id="accessibility-toolbar", className="accessibility-toolbar")


def create_screen_reader_summary(primary_metrics: dict) -> html.Div:
    """
    Create a screen reader-friendly summary of key metrics.
    
    Args:
        primary_metrics: Dictionary of primary metric values
    
    Returns:
        HTML Div with screen reader optimized content
    """
    return html.Div([
        html.H2("Dashboard Summary", className="visually-hidden"),
        html.Div([
            html.P(f"Extraction Accuracy: {primary_metrics.get('extraction_accuracy', 0):.1f}%", 
                   className="visually-hidden"),
            html.P(f"Document Accuracy: {primary_metrics.get('document_accuracy', 0):.1f}%", 
                   className="visually-hidden"),
            html.P(f"All Fields Accuracy: {primary_metrics.get('all_fields_accuracy', 0):.1f}%", 
                   className="visually-hidden")
        ], **{"aria-live": "polite", "aria-atomic": "true"})
    ], id="screen-reader-summary", className="sr-only")


def get_accessibility_css_classes(accessibility_state: dict) -> str:
    """
    Generate CSS classes based on accessibility state.
    
    Args:
        accessibility_state: Dictionary with accessibility settings
    
    Returns:
        String of CSS classes to apply
    """
    classes = []
    
    if accessibility_state.get("high_contrast", False):
        classes.append("high-contrast-mode")
    
    text_size = accessibility_state.get("text_size", "normal")
    classes.append(f"text-size-{text_size}")
    
    if accessibility_state.get("colorblind_mode", False):
        classes.append("colorblind-friendly")
    
    if accessibility_state.get("screen_reader_mode", False):
        classes.append("screen-reader-mode")
    
    return " ".join(classes)


def create_skip_navigation() -> html.Div:
    """
    Create skip navigation links for keyboard users.
    
    Returns:
        HTML Div with skip links
    """
    return html.Div([
        html.A("Skip to main content", 
               href="#main-content", 
               className="skip-link visually-hidden-focusable"),
        html.A("Skip to navigation", 
               href="#navigation", 
               className="skip-link visually-hidden-focusable"),
        html.A("Skip to accessibility options", 
               href="#accessibility-toolbar", 
               className="skip-link visually-hidden-focusable")
    ], className="skip-navigation")