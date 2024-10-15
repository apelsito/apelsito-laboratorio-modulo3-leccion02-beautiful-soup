# Importamos las librerías que necesitamos

# Librerías de extracción de datos
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests

# Tratamiento de datos
# -----------------------------------------------------------------------
import pandas as pd
import numpy as np
import datetime


def web_response(url):
    response = requests.get(url)
    code = response.status_code
    if code == 200:
        print(f"Respuesta recibida: {code}")
        return response
    else:
        print(f"Error, respuesta recibida: {code}")
        print(f"Ha fallado la url: {url}")
        return np.nan

def convert_to_soup(tosoupcontent):
    soup = BeautifulSoup(tosoupcontent.content, "html.parser")
    return soup

def obtain_elements(searchresultlist):
    element_operation = [element.getText() for element in searchresultlist]
    return element_operation

def format_dimension(dimension):
    operation = dimension.replace("\n","").replace(" (cm)","")
    return operation

search= 'a",{"class":"title"}'
def obtain_name(soup,search):
    lista_nombre_atrezo = soup.findAll(search)
    nombre_atrezo = obtain_elements(lista_nombre_atrezo)
    return nombre_atrezo

search= '"a",{"class":"tag"}'
def obtain_category(soup,search):
    lista_categoria_atrezo = soup.findAll(search)
    categoria_atrezo = obtain_elements(lista_categoria_atrezo)
    return categoria_atrezo

def obtain_section(soup,search):
    return

search = '"div",{"class":"article-container style-1"}'
def obtain_description(soup,search):
    lista_descripcion_atrezo = soup.findAll(search)
    descripcion_atrezo = obtain_elements(lista_descripcion_atrezo)
    return descripcion_atrezo

search = '"div",{"class":"price"}'
def obtain_dimensions(soup,search):
    lista_dimensiones_atrezo = soup.findAll(search)
    dimensiones_atrezo = obtain_elements(lista_dimensiones_atrezo)
    dimensiones = list(map(format_dimension,dimensiones_atrezo))
    return dimensiones
    