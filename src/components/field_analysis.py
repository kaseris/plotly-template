"""
Field Analysis component with scatter plots and field presence visualizations.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def create_scatter_plots() -> html.Div:
    """
    Create side-by-side scatter plots showing accuracy vs airline volume.
    
    Returns:
        HTML Div containing two scatter plots
    """
    # Generate sample data for scatter plots
    np.random.seed(42)
    n_airlines = 50
    
    # Sample data for volumes (x-axis, 0-80 range)
    volumes = np.random.randint(1, 80, n_airlines)
    
    # Accurate Extraction % with some correlation to volume
    accurate_extraction = np.random.beta(7, 2, n_airlines) * 0.6 + 0.4  # Range 0.4-1.0
    # Add slight negative correlation with volume (higher volume = slightly lower accuracy)
    accurate_extraction = accurate_extraction - (volumes / 200.0)
    accurate_extraction = np.clip(accurate_extraction, 0.4, 1.0)
    
    # Complete Accurate Extraction % (generally lower than accurate extraction)
    complete_accurate = accurate_extraction * np.random.uniform(0.7, 0.95, n_airlines)
    complete_accurate = np.clip(complete_accurate, 0.4, 1.0)
    
    # Create first scatter plot - Accurate Extraction
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=volumes,
        y=accurate_extraction,
        mode='markers',
        marker=dict(
            color='#1f77b4',  # Blue color to match existing theme
            size=6,
            opacity=0.7
        ),
        name='Airlines',
        hovertemplate='<b>Volume:</b> %{x}<br><b>Accurate Extraction:</b> %{y:.2%}<extra></extra>'
    ))
    
    fig1.update_layout(
        title=dict(
            text="Accurate Extraction % by Airline Volume",
            font={'size': 16, 'family': 'Inter, sans-serif', 'color': '#212529'}
        ),
        xaxis=dict(
            title="Count",
            range=[0, 80],
            showgrid=True,
            gridcolor='#e9ecef'
        ),
        yaxis=dict(
            title="Accurate Extraction %",
            range=[0.4, 1.0],
            tickformat='.1%',
            showgrid=True,
            gridcolor='#e9ecef'
        ),
        height=350,
        margin=dict(l=60, r=20, t=50, b=50),
        font={'family': 'Inter, sans-serif', 'size': 12, 'color': '#212529'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        showlegend=False
    )
    
    # Create second scatter plot - Complete Accurate Extraction
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=volumes,
        y=complete_accurate,
        mode='markers',
        marker=dict(
            color='#1f77b4',  # Same blue color for consistency
            size=6,
            opacity=0.7
        ),
        name='Airlines',
        hovertemplate='<b>Volume:</b> %{x}<br><b>Complete Accurate:</b> %{y:.2%}<extra></extra>'
    ))
    
    fig2.update_layout(
        title=dict(
            text="Complete Accurate Extraction % by Airline Volume",
            font={'size': 16, 'family': 'Inter, sans-serif', 'color': '#212529'}
        ),
        xaxis=dict(
            title="Count",
            range=[0, 80],
            showgrid=True,
            gridcolor='#e9ecef'
        ),
        yaxis=dict(
            title="Complete Accurate Extraction %",
            range=[0.4, 1.0],
            tickformat='.1%',
            showgrid=True,
            gridcolor='#e9ecef'
        ),
        height=350,
        margin=dict(l=60, r=20, t=50, b=50),
        font={'family': 'Inter, sans-serif', 'size': 12, 'color': '#212529'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        showlegend=False
    )
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig1, config={'displayModeBar': False})
            ], width=6, className="pe-2"),
            dbc.Col([
                dcc.Graph(figure=fig2, config={'displayModeBar': False})
            ], width=6, className="ps-2")
        ], className="g-0")
    ], className="mb-4")


def create_field_presence_gauges() -> html.Div:
    """
    Create three semicircle gauges for field presence metrics.
    Uses consistent styling with accuracy overview gauges.
    
    Returns:
        HTML Div containing gauge charts
    """
    # Sample data from the image (convert to percentage values)
    field_data = {
        'Flight Origin Present': 95.0,
        'Departure Date Present': 94.0,
        'Flight Number Present': 97.0
    }
    
    gauges = []
    for field_name, value in field_data.items():
        # Determine gauge color and status based on thresholds (same as accuracy overview)
        thresholds = {'excellent': 90, 'good': 75, 'bad': 0}
        
        if value >= thresholds['excellent']:
            gauge_color = '#28a745'  # Green
            status_text = 'Excellent'
        elif value >= thresholds['good']:
            gauge_color = '#ffc107'  # Yellow
            status_text = 'Good'
        else:
            gauge_color = '#dc3545'  # Red
            status_text = 'Bad'
        
        # Create gauge with styling matching accuracy overview
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            number={'suffix': '%'},  # Display as percentage
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': field_name, 'font': {'size': 18, 'family': 'Arial, sans-serif'}},
            gauge={
                'axis': {
                    'range': [0, 100.0],  # 0-100% range
                    'tickwidth': 1,
                    'tickcolor': "#333"
                },
                'bar': {'color': gauge_color, 'thickness': 0.3},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#ccc",
                'steps': [
                    {'range': [0, thresholds['good']], 'color': '#ffebee'},  # Bad: 0-75
                    {'range': [thresholds['good'], thresholds['excellent']], 'color': '#fff3cd'},  # Good: 75-90
                    {'range': [thresholds['excellent'], 100.0], 'color': '#d4edda'}  # Excellent: 90+
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': thresholds['excellent']
                }
            }
        ))
        
        # Add status annotation - positioned lower to avoid overlap (same as accuracy overview)
        fig.add_annotation(
            x=0.5, y=-0.1,
            text=f"<b>{status_text}</b>",
            showarrow=False,
            font={'size': 14, 'color': gauge_color, 'family': 'Arial, sans-serif'},
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor=gauge_color,
            borderwidth=1,
            borderpad=4
        )
        
        # Apply same layout styling as accuracy overview
        fig.update_layout(
            width=350,
            height=280,  # Same height as accuracy overview gauges
            margin=dict(l=20, r=20, t=60, b=40),  # Same margins with space for annotation
            font={'color': "#333", 'family': 'Arial, sans-serif'},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        gauges.append(
            dbc.Col([
                dcc.Graph(figure=fig, config={'displayModeBar': False}, className="gauge-chart")
            ], width=12, md=6, lg=4, className="mb-2")  # Same responsive breakpoints as accuracy overview
        )
    
    return html.Div([
        dbc.Row(gauges, className="g-2 justify-content-center")  # Same spacing as accuracy overview
    ], className="mb-4")


def create_document_fields_analysis() -> html.Div:
    """
    Create pie chart and legend showing document counts by fields present.
    
    Returns:
        HTML Div containing pie chart and legend
    """
    # Sample data based on the image
    field_counts = {
        'All 3 Fields': 850,
        '2 Fields': 120,
        '1 Field': 25,
        '0 Fields': 5
    }
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=list(field_counts.keys()),
        values=list(field_counts.values()),
        hole=0.3,  # Make it a donut chart
        marker=dict(
            colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],  # Blue dominant as shown in image
            line=dict(color='white', width=2)
        ),
        textinfo='none',  # Hide text on pie slices
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(
            text="Document Counts By Fields Present",
            font={'size': 16, 'family': 'Inter, sans-serif', 'color': '#212529'},
            x=0.5
        ),
        height=250,
        margin=dict(l=20, r=20, t=60, b=20),
        font={'family': 'Inter, sans-serif', 'size': 12, 'color': '#212529'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False  # We'll create custom legend
    )
    
    # Create custom legend
    legend_items = []
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, (label, count) in enumerate(field_counts.items()):
        legend_items.append(
            html.Div([
                html.Div(
                    style={
                        'width': '15px',
                        'height': '15px',
                        'backgroundColor': colors[i],
                        'display': 'inline-block',
                        'marginRight': '8px',
                        'borderRadius': '2px'
                    }
                ),
                html.Span(f"{i} - {count}", style={'fontSize': '14px'})
            ], className="d-flex align-items-center mb-2")
        )
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig, config={'displayModeBar': False})
            ], width=8),
            dbc.Col([
                html.Div([
                    html.H6("Number of Fields Present", 
                           className="mb-3",
                           style={'fontWeight': '600', 'color': '#212529'}),
                    html.Div(legend_items)
                ], className="mt-3")
            ], width=4)
        ], className="align-items-center")
    ], className="mb-4")


def create_field_analysis_tab() -> html.Div:
    """
    Create the complete field analysis tab content.
    
    Returns:
        HTML Div containing all field analysis visualizations
    """
    return html.Div([
        # Title section
        html.Div([
            html.H2("Field Analysis Dashboard", 
                   className="text-center mb-4",
                   style={'fontWeight': '600', 'color': '#212529'})
        ]),
        
        # Scatter plots section
        html.Div([
            html.H4("Accuracy vs Airline Volume", 
                   className="mb-3",
                   style={'fontWeight': '500', 'color': '#212529'}),
            create_scatter_plots()
        ], className="mb-5"),
        
        # Field presence gauges section  
        html.Div([
            html.H4("Field Presence Metrics", 
                   className="mb-3 text-center",
                   style={'fontWeight': '500', 'color': '#212529'}),
            create_field_presence_gauges()
        ], className="mb-5"),
        
        # Document fields analysis section
        html.Div([
            html.H4("Document Field Coverage", 
                   className="mb-3",
                   style={'fontWeight': '500', 'color': '#212529'}),
            create_document_fields_analysis()
        ], className="mb-4")
        
    ], className="p-3")