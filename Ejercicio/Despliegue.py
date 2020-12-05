#from urllib.request import urlopen
#from zipfile import ZipFile
#from io import BytesIO
#import shapefile
#import geopandas as geopandas
#from shapely.geometry import shape  
import pandas as pd
#import requests
import matplotlib.pyplot as plt
#from matplotlib.collections import PatchCollection
#from matplotlib.patches import Circle
#from IPython.display import HTML, display_html, display
import seaborn as sns
import numpy as np
#from matplotlib import cm
#from matplotlib import colors
#import ipywidgets as widgets
#from ipywidgets import interact, interactive
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash
import plotly.graph_objs as go
import plotly.express as px
#Carga base de datos

url1="https://raw.githubusercontent.com/acabezad/Dashboard/main/snies_Consolidado_2015_a_2018_p1.csv"
df = pd.read_csv(url1,  sep=';',  encoding='latin-1')

#url2="https://raw.githubusercontent.com/acabezad/Dashboard/main/snies_Consolidado_2015_a_2018_p2.csv"
#df2 = pd.read_csv(url2,  sep=';',  encoding='latin-1')

#url3="https://raw.githubusercontent.com/acabezad/Dashboard/main/snies_Consolidado_2015_a_2018_p2.csv"
#df3 = pd.read_csv(url3,  sep=';',  encoding='latin-1')

#url4="https://raw.githubusercontent.com/acabezad/Dashboard/main/snies_Consolidado_2015_a_2018_p2.csv"
#df4 = pd.read_csv(url4,  sep=';',  encoding='latin-1')

#df = pd.concat([df1, df2, df3, df4], axis=0)

#Reenombrar titulos de la base de datos
df2= df.rename(columns={'Código de \nla Institución  ':'COD_INSTITUCION',
                       'IES PADRE':'IES_PADRE',
                       'Institución de Educación Superior (IES)':'INSTITUCION',
                       'Principal\n o\nSeccional':'PRINCIPAL_SECCIONAL',
                       'Sector IES':'SECOTR_IES',
                       'Caracter IES':'CARACTER_IES',
                       'Código del \ndepartamento\n(IES)':'DPTO',
                       'Departamento de \ndomicilio de la IES':'DPTO_IES',
                       'Código del \nMunicipio\n(IES)':'COD_MUNICIPIO_IES',
                       'Municipio de\ndomicilio de la IES':'MUNICIPIO_IES',
                       'Código \nSNIES del\nprograma':'CODIGO_PROGRAMA',
                       'Programa Académico':'PROGRAMA_ACADEMICO',
                       'Nivel Académico':'NIVEL_ACADEMICO',
                       'Nivel de Formación' :'NIVEL_FORMACION',
                       'Metodología':'METODOLOGIA',
                       'Área de Conocimiento':'AREA_CONOCIMIENTO',
                       'Núcleo Básico del Conocimiento (NBC)':'NUCLEO_CONOCIMIENTO',
                       'Código del \nDepartamento\n(Programa)':'COD_DPTO_PROGRAMA',
                       'Departamento de oferta del programa':'DPTO_PROGRAMA',
                       'Código del \nMunicipio\n(Programa)':'COD_MUNICIPIO_PROGRAMA',
                       'Municipio de oferta del programa':'MUNICIPIO_PROGRAMA',
                       'Id Género':'ID_GENERO',
                       'Género':'GENERO' ,
                       'Matriculados':'MATRICULADOS'
                      })


# Todos los campos los vuelve minuscula
df2=df2.apply(lambda x: x.str.lower() if(x.dtype == "object") else x)

#Ajusta Area de conocimiento
df2["GENERO"]=[i.replace("femenino","mujer") for i in df2["GENERO"]]

df2["GENERO"]=[i.replace("masculino","hombre") for i in df2["GENERO"]]


df2["NIVEL_FORMACION"]=[i.replace("formacion tecnica profesional","tecnica") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("especialización médico quirúrgica","especializacion") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("especialización universitaria","especializacion") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("maestría","maestria") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("tecnológica","tecnologica") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("formación técnica profesional","tecnica") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("especialización tecnologica","especializacion") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("especialización técnico profesional","especializacion") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("especialización tecnológica","especializacion") for i in df2["NIVEL_FORMACION"]]



df2["CARACTER_IES"]=[i.replace("institución técnica profesional","institucion tecnica profesional") for i in df2["CARACTER_IES"]]
df2["CARACTER_IES"]=[i.replace("institución tecnológica","institucion tecnologica") for i in df2["CARACTER_IES"]]
df2["CARACTER_IES"]=[i.replace("institución universitaria/escuela tecnológica","institucion universitaria/escuela tecnologica") for i in df2["CARACTER_IES"]]


df2.METODOLOGIA=df2.METODOLOGIA.replace({"virtual":"distancia (virtual)"})


df2["AREA_CONOCIMIENTO"]=[i.replace("ingeniería, arquitectura, urbanismo y afines","ingenieria arquitectura urbanismo y afines") for i in df2["AREA_CONOCIMIENTO"]]
df2["AREA_CONOCIMIENTO"]=[i.replace("matemáticas y ciencias naturales","matematicas y ciencias naturales") for i in df2["AREA_CONOCIMIENTO"]]
df2["AREA_CONOCIMIENTO"]=[i.replace("agronomía, veterinaria y afines","agronomia veterinaria y afines") for i in df2["AREA_CONOCIMIENTO"]]
df2["AREA_CONOCIMIENTO"]=[i.replace("ciencias de la educación","ciencias de la educacion") for i in df2["AREA_CONOCIMIENTO"]]
df2["AREA_CONOCIMIENTO"]=[i.replace("economía, administración, contaduría y afines","economia administracion contaduria y afines") for i in df2["AREA_CONOCIMIENTO"]]


af =pd.DataFrame(df2.groupby(['lat', 'lon', 'Id_Sector', "NIVEL_FORMACION", "DPTO_IES", "METODOLOGIA", 'GENERO', "AREA_CONOCIMIENTO", "Año", "SECOTR_IES"])['MATRICULADOS'].sum().reset_index())


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
