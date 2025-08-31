#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 10:07:18 2024

@author: root
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd





# Data
data = {
    'Sector': ['Manager', 'Manager', 'Manager', 'Manager', 'Marketing', 'Marketing', 'Marketing','Vazio'],
    'Porque não efetuamos o Pedido?': ['Preço', 'Atendimento', 'Fidelidade com concorrente', 'Pazo de entrega', 
              'Inicio de relacionamento', 'Variedade de produtos', 'Qualidade do produto','vazio']
}
datas = pd.DataFrame(data)
tuples = [(source,target) for source, target in zip(data['Porque não efetuamos o Pedido?'],data['Sector'])]
datas['tuples'] = tuples


conc = pd.read_pickle('/private/var/root/Target/Pickles/conc_2.pkl')
df = conc['Nome do Representante'].value_counts().to_frame().reset_index()

# Create Dash app
app = dash.Dash(__name__)

# Layout with a graph and a div to display hover/click info
app.layout = html.Div([
    dcc.Graph(
        id='example-graph',
        figure=px.bar(df, x="Nome do Representante", y="count"),
    ),
    html.Div([dcc.Graph(id='output_1'),
    ], style={'display': 'inline-block', 'width': '35%'}),
    html.Div([dcc.Graph(id='output_2'),
    ], style={'display': 'inline-block', 'width': '35%'}),
    html.Div([dcc.Graph(id='output_3'),
    ], style={'display': 'inline-block', 'width': '35%'}),
    html.Div([dcc.Graph(id='output_4'),
    ], style={'display': 'inline-block', 'width': '35%'}),
    html.Div([dcc.Graph(id='output_5'),
    ], style={'display': 'inline-block', 'width': '35%'}),
    html.Div([dcc.Graph(id='output_6'),
    ], style={'display': 'inline-block', 'width': '35%'}),
    html.Div([dcc.Graph(id='output_7'),
    ], style={'display': 'inline-block', 'width': '35%'}),
    html.Div([dcc.Graph(id='output_8'),
    ], style={'display': 'inline-block', 'width': '35%'}),
    html.Div([dcc.Graph(id='output_9'),
    ], style={'display': 'inline-block', 'width': '35%'}),
    
        
    html.Div(id='click-output')
])




# 1 - Callback for hoverData 
@app.callback(
    Output('output_1', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Porque não efetuamos o Pedido?'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 2 - Callback for hoverData 
@app.callback(
    Output('output_2', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Conhece alguma marca do GRUPO DVG'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 3 - Callback for hoverData 
@app.callback(
    Output('output_3', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Porque parou de comprar?'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 4 - Callback for hoverData 
@app.callback(
    Output('output_4', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Já compou da TUBOZAN'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 5 - Callback for hoverData 
@app.callback(
    Output('output_5', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Regional do Representante'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 6 - Callback for hoverData 
@app.callback(
    Output('output_6', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Fez o pedido'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 7 - Callback for hoverData 
@app.callback(
    Output('output_7', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Qual concorrente?'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 8 - Callback for hoverData 
@app.callback(
    Output('output_8', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Já compou da TUBOZAN'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 9 - Callback for hoverData 
@app.callback(
    Output('output_9', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Porque não efetuamos o Pedido?'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        selected = set(dff.loc[:,frame].to_list())
        dt     = datas.query(" `Porque não efetuamos o Pedido?` in @selected ")
        
        # Create a mapping for the unique labels
        labels = list(set(dt['Sector'].to_list() + dt['Porque não efetuamos o Pedido?'].to_list()))

        # Map sectors and issues to their respective indices
        label_map = {label: i for i, label in enumerate(labels)}

        # Create the Sankey diagram data
        source_indices = [label_map[sector] for sector in dt['Sector']]
        target_indices = [label_map[issue] for issue in dt['Porque não efetuamos o Pedido?']]

        # Assign default values for the links
        values = [1] * len(source_indices)

        # Create the Sankey chart
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=values
            )
        ))

        # Set the title and display the figure
        fig.update_layout(title_text="Tomada de decisão", font_size=10)
        return fig
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")



if __name__ == '__main__':
    app.run_server(debug=True)
    
