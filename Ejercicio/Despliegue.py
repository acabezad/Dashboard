from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
#import shapefile
import geopandas as geopandas
#from shapely.geometry import shape  
import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
from IPython.display import HTML, display_html, display
import seaborn as sns
import numpy as np
from matplotlib import cm
from matplotlib import colors
import ipywidgets as widgets
from ipywidgets import interact, interactive
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash
import plotly.graph_objs as go
import plotly.express as px


#Carga base de datos

url1="export_dataframe.csv"
af = pd.read_csv(url1,  sep=',',  encoding="utf-8")

app = dash.Dash()

       
available_indicators = af['DPTO_IES'].unique()
Año = af['Año'].unique()

    
colors = {'background': '#E5E7E9', 'text': '#481099' }


#diseño del app
app.layout = html.Div([
    html.H1(children='Dashboard SNIES Colombia', style={ 'textAlign': 'center', 'color': colors['text'] }),
    html.Div([ 
    dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=None,
    style={"display": "inline-block", 'width': '49%','height': '40px'}
            ),
    dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in Año],
                value=None,
    style={"display": "inline-block", 'width': '49%','height': '40px'}
            ),
        html.Div([
    dcc.Graph(id='f1', style={"display": "inline-block", 'width': '100%', "border-style": "dashed", "border-width": "1px", "color": "blue" }),     
        ])]),
    
    html.Div([
    dcc.Graph(id='f2')],
        style={"display": "inline-block", 'width': '49.2%', "border-style": "dashed", "border-width": "1px", "color": "blue" }),

    html.Div([
    dcc.Graph(id='f3')],
        style={'display': 'inline-block', 'width': '49.2%', "border-style": "dashed", "border-width": "1px", "color": "blue"}),
    
    html.Div([
    dcc.Graph(id='f4')],
        style={"display": "inline-block", 'width': '100%', "border-style": "dashed", "border-width": "1px", "color": "blue" }),

    
])


@app.callback(
    Output('f1', 'figure'),
    Output('f2', 'figure'),
    Output('f3', 'figure'),
    Output('f4', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'))

def Mapa (xaxis,yaxis):
        
    if (xaxis == None and yaxis == None): 
        
        af3 =pd.DataFrame(af.groupby(["METODOLOGIA", "Año"])['MATRICULADOS'].sum().reset_index())
        
        af4 =pd.DataFrame(af.groupby(["AREA_CONOCIMIENTO", "SECOTR_IES"])['MATRICULADOS'].sum().reset_index())
        
        fig1 = px.scatter_mapbox(af, lat="lat", lon="lon", color="MATRICULADOS", size="MATRICULADOS",
                      color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=4,
                      mapbox_style="open-street-map", title='Distribución de Matriculados por Departamento')  
        
        fig2 = px.pie(af, values='MATRICULADOS', names='NIVEL_FORMACION', title='Distribución por Nivel de Formación')
        
        fig3 = px.line(af3, x="Año", y="MATRICULADOS", color="METODOLOGIA", title='Evolución de Metodologia de Estudio')
        
        fig4 = px.bar(af4, x="AREA_CONOCIMIENTO", y="MATRICULADOS", color="SECOTR_IES", title='Concentración de Área de Conocimiento')
        
        
    elif (xaxis != None and yaxis == None): 
        
        af2 = af[af['DPTO_IES']== xaxis]
        
        af3 =pd.DataFrame(af2.groupby(["METODOLOGIA", "Año"])['MATRICULADOS'].sum().reset_index())
        
        af4 =pd.DataFrame(af2.groupby(["AREA_CONOCIMIENTO", "SECOTR_IES"])['MATRICULADOS'].sum().reset_index())

        fig1 = px.scatter_mapbox(af2, lat="lat", lon="lon", color="MATRICULADOS", size="MATRICULADOS",
                      color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=4,
                      mapbox_style="open-street-map", title='Distribución de Matriculados por Departamento')
        
        fig2 = px.pie(af2, values='MATRICULADOS', names='NIVEL_FORMACION', title='Distribución por Nivel de Formación')
        
        fig3 = px.line(af3, x="Año", y="MATRICULADOS", color="METODOLOGIA", title='Evolución de Metodologia de Estudio')
        
        fig4 = px.bar(af4, x="AREA_CONOCIMIENTO", y="MATRICULADOS", color="SECOTR_IES", title='Concentración de Área de Conocimiento')

        
        
    elif (xaxis == None and yaxis != None): 
        
        af2 = af[af['Año']== yaxis]

        af3 =pd.DataFrame(af.groupby(["METODOLOGIA", "Año"])['MATRICULADOS'].sum().reset_index())
        
        af4 =pd.DataFrame(af2.groupby(["AREA_CONOCIMIENTO", "SECOTR_IES"])['MATRICULADOS'].sum().reset_index())

        fig1 = px.scatter_mapbox(af2, lat="lat", lon="lon", color="MATRICULADOS", size="MATRICULADOS",
                      color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=4,
                      mapbox_style="open-street-map", title='Distribución de Matriculados por Departamento')
        
        fig2 = px.pie(af2, values='MATRICULADOS', names='NIVEL_FORMACION', title='Distribución por Nivel de Formación')
        
        fig3 = px.line(af3, x="Año", y="MATRICULADOS", color="METODOLOGIA", title='Evolución de Metodologia de Estudio')
        
        fig4 = px.bar(af4, x="AREA_CONOCIMIENTO", y="MATRICULADOS", color="SECOTR_IES", title='Concentración de Área de Conocimiento')
        
    else:
    
        af2 = af[(af.DPTO_IES == xaxis) & (af.Año == yaxis)]
        
        af2_ = af[af['DPTO_IES']== xaxis]

        af3 =pd.DataFrame(af2_.groupby(["METODOLOGIA", "Año"])['MATRICULADOS'].sum().reset_index())
        
        af4 =pd.DataFrame(af2.groupby(["AREA_CONOCIMIENTO", "SECOTR_IES"])['MATRICULADOS'].sum().reset_index())

        fig1 = px.scatter_mapbox(af2, lat="lat", lon="lon", color="MATRICULADOS", size="MATRICULADOS",
                      color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=4,
                      mapbox_style="open-street-map", title='Distribución de Matriculados por Departamento')
        
        fig2 = px.pie(af2, values='MATRICULADOS', names='NIVEL_FORMACION', title='Distribución por Nivel de Formación')
        
        fig3 = px.line(af3, x="Año", y="MATRICULADOS", color="METODOLOGIA", title='Evolución de Metodologia de Estudio')
        
        fig4 = px.bar(af4, x="AREA_CONOCIMIENTO", y="MATRICULADOS", color="SECOTR_IES", title='Concentración de Área de Conocimiento')

        
    return fig1, fig2, fig3, fig4
  
app.run_server(debug=True, host='0.0.0.0', port=8050)
