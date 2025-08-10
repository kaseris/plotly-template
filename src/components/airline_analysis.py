"""
Airline Analysis component with histogram and paginated table.
"""

from dash import html, dcc, dash_table
import plotly.express as px
import pandas as pd


def create_airline_histogram() -> dcc.Graph:
    """
    Create histogram showing accuracy distribution by airline.
    
    Returns:
        Plotly Graph component with histogram
    """
    # Sample airline data based on the image
    airline_data = [
        'AY', 'UA', 'TG', 'AC', 'CX', 'QR', 'SQ', 'QF', 'LX', 'UO', 'BA', 'JQ', 'EK', 'MH', 'AF',
        'HX', 'TK', 'AK', 'CA', 'MU', 'AA', 'LE', 'VA', 'TR', 'ZH', 'OD', 'DY', 'CZ'
    ]
    
    # Simulate accuracy values matching the histogram pattern
    accuracy_values = [
        0.95, 0.92, 0.90, 0.88, 0.86, 0.84, 0.82, 0.80, 0.78, 0.76,
        0.74, 0.72, 0.70, 0.68, 0.66, 0.64, 0.62, 0.60, 0.58, 0.56,
        0.54, 0.52, 0.50, 0.48, 0.46, 0.44, 0.42, 0.40, 0.38, 0.36
    ][:len(airline_data)]
    
    # Create DataFrame
    df = pd.DataFrame({
        'Airline': airline_data,
        'Accuracy': accuracy_values,
        'Complete_Accuracy': [acc * 0.9 for acc in accuracy_values]  # Slightly lower
    })
    
    # Create grouped bar chart with bars side by side
    fig = px.bar(
        df, 
        x='Airline', 
        y=['Accuracy', 'Complete_Accuracy'],
        title='Accurate and Complete Accurate Extraction % for Airlines with 20+ Samples',
        labels={'value': 'Extraction %', 'variable': 'Metric Type'},
        color_discrete_map={'Accuracy': '#1f77b4', 'Complete_Accuracy': '#ff7f0e'},
        barmode='group',  # This creates side-by-side bars instead of stacked
        height=500
    )
    
    # Update layout to match image style
    fig.update_layout(
        xaxis_title='Airline',
        yaxis_title='Extraction %',
        yaxis=dict(range=[0, 1.0]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(t=80, b=50, l=50, r=50)
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_airline_table(page_size: int = 10) -> html.Div:
    """
    Create paginated table with airline extraction data.
    
    Args:
        page_size: Number of rows per page
    
    Returns:
        HTML Div containing table and pagination
    """
    # Sample detailed airline data based on the second image
    airline_data = [
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
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(airline_data)
    
    # Create DataTable with pagination
    table = dash_table.DataTable(
        data=df.to_dict('records'),
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
        page_size=page_size,
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
    
    return html.Div([
        html.H4("Airline Extraction Performance Details", 
                className="mb-3",
                style={'fontWeight': '600', 'color': '#212529'}),
        table
    ])


def create_airline_analysis_tab() -> html.Div:
    """
    Create the complete airline analysis tab content.
    
    Returns:
        HTML Div containing histogram and table
    """
    return html.Div([
        # Histogram section
        html.Div([
            create_airline_histogram()
        ], className="mb-4"),
        
        # Table section
        html.Div([
            create_airline_table()
        ], className="mb-4")
    ], className="p-3")