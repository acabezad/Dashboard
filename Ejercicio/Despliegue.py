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

url="https://raw.githubusercontent.com/acabezad/Dashboard/main/snies_Consolidado_2015_a_2018_TMP.csv"
df = pd.read_csv(url,  sep=';',  encoding='latin-1')

#Valida cargue
print (df.dtypes)


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


print (df2.GENERO.unique())

#Ajusta Area de conocimiento
df2["GENERO"]=[i.replace("femenino","mujer") for i in df2["GENERO"]]

df2["GENERO"]=[i.replace("masculino","hombre") for i in df2["GENERO"]]
print (df2.GENERO.unique())


df2["NIVEL_FORMACION"]=[i.replace("formacion tecnica profesional","tecnica") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("especialización médico quirúrgica","especializacion") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("especialización universitaria","especializacion") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("maestría","maestria") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("tecnológica","tecnologica") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("formación técnica profesional","tecnica") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("especialización tecnologica","especializacion") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("especialización técnico profesional","especializacion") for i in df2["NIVEL_FORMACION"]]
df2["NIVEL_FORMACION"]=[i.replace("especialización tecnológica","especializacion") for i in df2["NIVEL_FORMACION"]]
print (df2.NIVEL_FORMACION.unique())


df2["CARACTER_IES"]=[i.replace("institución técnica profesional","institucion tecnica profesional") for i in df2["CARACTER_IES"]]
df2["CARACTER_IES"]=[i.replace("institución tecnológica","institucion tecnologica") for i in df2["CARACTER_IES"]]
df2["CARACTER_IES"]=[i.replace("institución universitaria/escuela tecnológica","institucion universitaria/escuela tecnologica") for i in df2["CARACTER_IES"]]
print (df2.CARACTER_IES.unique())


df2.METODOLOGIA=df2.METODOLOGIA.replace({"virtual":"distancia (virtual)"})
print (df2.METODOLOGIA.unique())

df2["AREA_CONOCIMIENTO"]=[i.replace("ingeniería, arquitectura, urbanismo y afines","ingenieria arquitectura urbanismo y afines") for i in df2["AREA_CONOCIMIENTO"]]
df2["AREA_CONOCIMIENTO"]=[i.replace("matemáticas y ciencias naturales","matematicas y ciencias naturales") for i in df2["AREA_CONOCIMIENTO"]]
df2["AREA_CONOCIMIENTO"]=[i.replace("agronomía, veterinaria y afines","agronomia veterinaria y afines") for i in df2["AREA_CONOCIMIENTO"]]
df2["AREA_CONOCIMIENTO"]=[i.replace("ciencias de la educación","ciencias de la educacion") for i in df2["AREA_CONOCIMIENTO"]]
df2["AREA_CONOCIMIENTO"]=[i.replace("economía, administración, contaduría y afines","economia administracion contaduria y afines") for i in df2["AREA_CONOCIMIENTO"]]
print (df2.AREA_CONOCIMIENTO.unique())

nombres=list(df2.NIVEL_FORMACION.unique())
print(nombres)
tb=pd.DataFrame(df2.groupby('NIVEL_FORMACION')['MATRICULADOS'].sum())
manzanas=list(tb.MATRICULADOS)


print (df2.dtypes)


app = dash.Dash()


fig = px.pie(df2, values='MATRICULADOS', names='NIVEL_FORMACION', title='FIGURA 1')

fig2 = px.bar(df2, x="AREA_CONOCIMIENTO", y="MATRICULADOS", color="SECOTR_IES")

fig3 = px.line(df2, x="Año", y="MATRICULADOS", color="METODOLOGIA")

fig4 = px.line(df2, x="Año", y="MATRICULADOS", color="METODOLOGIA")


#diseño del app
app.layout = html.Div([
    
    
    html.Div([
    dcc.Graph(figure=fig)],
        style={"display": "inline-block", 'width': '49%', "border-style": "dashed", "border-width": "1px", "color": "blue" }),

    html.Div([
    dcc.Graph(figure=fig2)],
        style={'display': 'inline-block', 'width': '49%', "border-style": "dashed", "border-width": "1px", "color": "blue"}),
    
    html.Div([
    dcc.Graph(figure=fig3)],
        style={"display": "inline-block", 'width': '49%', "border-style": "dashed", "border-width": "1px", "color": "blue" }),

    html.Div([
    dcc.Graph(figure=fig4)],
        style={'display': 'inline-block', 'width': '49%', "border-style": "dashed", "border-width": "1px", "color": "blue"}),      
        
        ])

app.run_server(port="8051")
