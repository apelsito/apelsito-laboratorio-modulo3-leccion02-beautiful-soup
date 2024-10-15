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

def format_section(section):

    operation = section.strip().replace("\xa0\xa0"," ")
    return operation


def obtain_name(soup):
    lista_nombre_atrezo = soup.findAll('a',{'class':'title'})
    nombre_atrezo = obtain_elements(lista_nombre_atrezo)
    return nombre_atrezo


def obtain_category(soup):
    lista_categoria_atrezo = soup.findAll('div',{'class':'product-slide-entry shift-image'})
    categoria_atrezo = [categoria.contents[2].getText() for categoria in lista_categoria_atrezo]
    
    return categoria_atrezo


def obtain_section(soup):
    lista_seccion_atrezo = soup.findAll("div",{"class":"cat-sec-box"})
    seccion_atrezo = [element.getText() for element in lista_seccion_atrezo]
    seccion = list(map(format_section,seccion_atrezo))
    return seccion


def obtain_description(soup):
    lista_descripcion_atrezo = soup.findAll("div",{"class":"product-slide-entry shift-image"})
    descripcion_atrezo = [descripcion.getText() for descripcion in lista_descripcion_atrezo]
    descripcion = list(map(format_dimension,descripcion_atrezo))
    return descripcion


def obtain_dimensions(soup):
    lista_dimensiones_atrezo = soup.findAll("div",{"class":"price"})
    dimensiones_atrezo = obtain_elements(lista_dimensiones_atrezo)
    dimensiones = [format_dimension(dimension) for dimension in dimensiones_atrezo]
    return dimensiones


def obtain_image_url(soup):
    lista_imagen_atrezo = soup.findAll("div",{"class":"product-image"})
    imagenes_atrezo = [f"https://atrezzovazquez.es/{imagen.contents[0].get('src')}" for imagen in lista_imagen_atrezo]
    return imagenes_atrezo

def create_df(webpage):
    contact = web_response(webpage)
    if contact.status_code == 200:
        soup = convert_to_soup(contact)
        name_list = obtain_name(soup)
        category_list = obtain_category(soup)
        section_list = obtain_section(soup)
        description_list = obtain_description(soup)
        dimension_list = obtain_dimensions(soup)
        image_list = obtain_image_url(soup)
        
        df = pd.DataFrame({
            "Nombre": name_list,
            "Categoría": category_list,
            "Sección": section_list,
            "Descripción": description_list,
            "Dimensiones": dimension_list,
            "URL Imágenes": image_list
        })
        return df
    else:
        return
    
