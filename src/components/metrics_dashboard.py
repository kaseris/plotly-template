"""
Metrics Dashboard component displaying document extraction statistics.
"""

from dash import html
import dash_bootstrap_components as dbc
from typing import Dict, List, Optional, Union


def create_metric_card(
    title: str,
    value: int,
    subtitle: Optional[str] = None,
    color: str = "primary"
) -> dbc.Card:
    """
    Create a metric card displaying a number with title.
    
    Args:
        title: Card title
        value: Numeric value to display
        subtitle: Optional subtitle text
        color: Bootstrap color theme
    
    Returns:
        Dash Bootstrap Components Card
    """
    card_style = {
        'backgroundColor': '#f8f9fa',
        'borderLeft': f'4px solid var(--bs-{color})',
        'color': '#212529'
    }
    
    card_body = [
        html.H6(title, className="mb-1 text-muted", 
                style={'fontSize': '0.8rem', 'fontWeight': '600'}),
        html.H3(f"{value:,}", className="mb-0",
                style={'fontSize': '2rem', 'fontWeight': '700', 'color': '#212529'})
    ]
    
    if subtitle:
        card_body.append(
            html.P(subtitle, className="text-muted mb-0 mt-1",
                   style={'fontSize': '0.7rem'})
        )
    
    return dbc.Card(
        dbc.CardBody(card_body, className="py-3 px-3"),
        className="h-100",
        style={
            **card_style,
            'border': '1px solid #dee2e6',
            'borderRadius': '8px'
        }
    )


def create_metric_group(
    cards: List[dbc.Card],
    group_title: Optional[str] = None,
    cards_per_row: int = 4,
    use_card_group: bool = False
) -> html.Div:
    """
    Create a group of metric cards with flexible layout options.
    
    Args:
        cards: List of metric cards to group
        group_title: Optional title for the group
        cards_per_row: Number of cards per row (1-12)
        use_card_group: Use CardGroup for equal heights (max 6 cards recommended)
    
    Returns:
        HTML Div containing the grouped cards
    """
    if use_card_group and len(cards) <= 6:
        # Use CardGroup for equal height cards
        group_content = dbc.CardGroup(cards)
    else:
        # Use responsive grid layout
        col_width = max(1, min(12, 12 // cards_per_row))
        card_cols = [
            dbc.Col(card, width=12, sm=6, lg=col_width, className="mb-3")
            for card in cards
        ]
        group_content = dbc.Row(card_cols, className="g-3")
    
    group_components = []
    if group_title:
        group_components.append(
            html.H4(group_title, 
                   className="mb-3 text-muted",
                   style={'fontWeight': '600', 'fontSize': '1.1rem'})
        )
    group_components.append(group_content)
    
    return html.Div(group_components, className="mb-4")


def create_metrics_dashboard(
    group_config: Optional[Dict] = None
) -> html.Div:
    """
    Create the complete metrics dashboard with document statistics.
    
    Args:
        group_config: Optional configuration for grouping cards
            Example: {
                "groups": [
                    {"title": "Document Metrics", "cards_per_row": 2, "use_card_group": False},
                    {"title": "Field Metrics", "cards_per_row": 4, "use_card_group": True}
                ]
            }
    
    Returns:
        HTML Div containing grouped metrics cards
    """
    # Sample data matching the image
    metrics_data = [
        {"title": "Doc Count", "value": 1986, "subtitle": "Total documents", "color": "info"},
        {"title": "Accurate Extraction", "value": 1598, "subtitle": "Successfully processed", "color": "success"},
        {"title": "Complete Accurate Extraction", "value": 1334, "subtitle": "Fully complete", "color": "primary"},
        {"title": "Automated Documents", "value": 1735, "subtitle": "Auto processed", "color": "warning"},
        {"title": "Fields Extracted", "value": 5644, "subtitle": "Total fields", "color": "secondary"},
        {"title": "Fields Possible", "value": 5958, "subtitle": "Available fields", "color": "dark"},
        {"title": "Fields Present", "value": 5676, "subtitle": "Fields in docs", "color": "info"},
        {"title": "Fields Correctly Extracted", "value": 5121, "subtitle": "Accurate fields", "color": "success"}
    ]
    
    # Create all metric cards
    all_cards = [
        create_metric_card(
            title=metric["title"],
            value=metric["value"],
            subtitle=metric["subtitle"],
            color=metric["color"]
        )
        for metric in metrics_data
    ]
    
    # Default grouping: Document metrics (4 cards) + Field metrics (4 cards)
    if group_config is None:
        group_config = {
            "groups": [
                {"title": "Document Metrics", "cards_per_row": 4, "use_card_group": False},
                {"title": "Field Metrics", "cards_per_row": 4, "use_card_group": False}
            ]
        }
    
    dashboard_components = [
        html.H3("Document Extraction Metrics", 
                className="mb-4 text-center",
                style={'fontWeight': '600', 'color': '#212529'})
    ]
    
    # Create groups based on configuration
    card_index = 0
    groups = group_config.get("groups", [])
    
    for group in groups:
        # Calculate cards per group
        cards_in_group = group.get("cards_per_row", 4)
        if group.get("use_card_group", False):
            cards_in_group = min(cards_in_group, 6)  # CardGroup limit
        
        # Get cards for this group
        group_cards = all_cards[card_index:card_index + cards_in_group]
        card_index += len(group_cards)
        
        if group_cards:
            metric_group = create_metric_group(
                cards=group_cards,
                group_title=group.get("title"),
                cards_per_row=group.get("cards_per_row", 4),
                use_card_group=group.get("use_card_group", False)
            )
            dashboard_components.append(metric_group)
    
    # Add any remaining cards as a single group
    if card_index < len(all_cards):
        remaining_cards = all_cards[card_index:]
        remaining_group = create_metric_group(
            cards=remaining_cards,
            cards_per_row=4
        )
        dashboard_components.append(remaining_group)
    
    return html.Div(dashboard_components, className="mb-4")