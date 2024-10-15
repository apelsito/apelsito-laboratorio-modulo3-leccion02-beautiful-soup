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
    """
    Realiza una solicitud GET a una URL dada y devuelve la respuesta si el estado es exitoso (200).

    Args:
        url (str): La URL a la que se realizará la solicitud GET.

    Returns:
        requests.Response: La respuesta de la solicitud si el código de estado es 200.
        np.nan: Devuelve np.nan si la respuesta no tiene un código de estado 200.

    Prints:
        Mensajes indicando el código de estado recibido o que la URL ha fallado si no es exitoso.
    """
    response = requests.get(url)
    code = response.status_code
    if code == 200:
        #print(f"Respuesta recibida: {code}")
        return response
    else:
        print(f"Error, respuesta recibida: {code}")
        print(f"Ha fallado la url: {url}")
        return np.nan

def convert_to_soup(tosoupcontent):
    """
    Convierte el contenido de una respuesta en un objeto BeautifulSoup para su análisis HTML.

    Args:
        tosoupcontent (requests.Response): La respuesta de una solicitud HTTP, cuyo contenido será convertido a un objeto BeautifulSoup.

    Returns:
        BeautifulSoup: Un objeto BeautifulSoup que permite analizar y extraer información del contenido HTML de la respuesta.
    """
    soup = BeautifulSoup(tosoupcontent.content, "html.parser")
    return soup


def obtain_elements(searchresultlist):
    """
    Extrae el texto de una lista de elementos HTML.

    Args:
        searchresultlist (list): Lista de objetos BeautifulSoup, generalmente obtenidos mediante métodos como findAll().

    Returns:
        list: Una lista de cadenas de texto, donde cada elemento es el texto extraído de los elementos HTML de la lista proporcionada.
    """
    element_operation = [element.getText() for element in searchresultlist]
    return element_operation

def format_dimension(dimension):
    """
    Formatea una cadena de texto que representa una dimensión, eliminando saltos de línea y la unidad '(cm)'.

    Args:
        dimension (str): Una cadena de texto que representa una dimensión, posiblemente con saltos de línea o la unidad '(cm)'.

    Returns:
        str: La cadena formateada, sin saltos de línea ni la unidad '(cm)'.
    """
    operation = dimension.replace("\n","").replace(" (cm)","")
    return operation

def format_section(section):
    """
    Formatea una cadena de texto que representa una sección, eliminando espacios en blanco al principio y al final, 
    y reemplazando caracteres de espacio no separables (\xa0) por espacios normales.

    Args:
        section (str): Una cadena de texto que representa una sección con posibles caracteres de espacio no separables (\xa0).

    Returns:
        str: La cadena formateada, con los espacios eliminados al principio y al final, y los caracteres de espacio no separables reemplazados por espacios normales.
    """
    operation = section.strip().replace("\xa0\xa0"," ")
    return operation


def obtain_name(soup):
    """
    Extrae los nombres de los elementos HTML que contienen la clase 'title' dentro de un objeto BeautifulSoup.

    Args:
        soup (BeautifulSoup): Un objeto BeautifulSoup que contiene el contenido HTML del cual se extraerán los nombres.

    Returns:
        list: Una lista de cadenas de texto que representan los nombres extraídos de los elementos con la clase 'title'.
    """
    lista_nombre_atrezo = soup.findAll('a',{'class':'title'})
    nombre_atrezo = obtain_elements(lista_nombre_atrezo)
    return nombre_atrezo


def obtain_category(soup):
    """
    Extrae las categorías de los elementos HTML que contienen la clase 'product-slide-entry shift-image' dentro de un objeto BeautifulSoup.

    Args:
        soup (BeautifulSoup): Un objeto BeautifulSoup que contiene el contenido HTML del cual se extraerán las categorías.

    Returns:
        list: Una lista de cadenas de texto que representan las categorías extraídas de los elementos con la clase 'product-slide-entry shift-image'.
    """
    lista_categoria_atrezo = soup.findAll('div',{'class':'product-slide-entry shift-image'})
    categoria_atrezo = [categoria.contents[2].getText() for categoria in lista_categoria_atrezo]
    
    return categoria_atrezo


def obtain_section(soup):
    """
    Extrae y formatea las secciones de los elementos HTML que contienen la clase 'cat-sec-box' dentro de un objeto BeautifulSoup.

    Args:
        soup (BeautifulSoup): Un objeto BeautifulSoup que contiene el contenido HTML del cual se extraerán las secciones.

    Returns:
        list: Una lista de cadenas de texto que representan las secciones extraídas y formateadas de los elementos con la clase 'cat-sec-box'.
    """
    lista_seccion_atrezo = soup.findAll("div",{"class":"cat-sec-box"})
    seccion_atrezo = [element.getText() for element in lista_seccion_atrezo]
    seccion = list(map(format_section,seccion_atrezo))
    return seccion


def obtain_description(soup):
    """
    Extrae y formatea las descripciones de los elementos HTML que contienen la clase 'product-slide-entry shift-image' dentro de un objeto BeautifulSoup.

    Args:
        soup (BeautifulSoup): Un objeto BeautifulSoup que contiene el contenido HTML del cual se extraerán las descripciones.

    Returns:
        list: Una lista de cadenas de texto que representan las descripciones extraídas y formateadas de los elementos con la clase 'product-slide-entry shift-image'.
    """
    lista_descripcion_atrezo = soup.findAll("div",{"class":"product-slide-entry shift-image"})
    descripcion_atrezo = [descripcion.getText() for descripcion in lista_descripcion_atrezo]
    descripcion = list(map(format_dimension,descripcion_atrezo))
    return descripcion


def obtain_dimensions(soup):
    """
    Extrae y formatea las dimensiones de los elementos HTML que contienen la clase 'price' dentro de un objeto BeautifulSoup.

    Args:
        soup (BeautifulSoup): Un objeto BeautifulSoup que contiene el contenido HTML del cual se extraerán las dimensiones.

    Returns:
        list: Una lista de cadenas de texto que representan las dimensiones extraídas y formateadas de los elementos con la clase 'price'.
    """
    lista_dimensiones_atrezo = soup.findAll("div",{"class":"price"})
    dimensiones_atrezo = obtain_elements(lista_dimensiones_atrezo)
    dimensiones = [format_dimension(dimension) for dimension in dimensiones_atrezo]
    return dimensiones


def obtain_image_url(soup):
    """
    Extrae las URLs de las imágenes de los elementos HTML que contienen la clase 'product-image' dentro de un objeto BeautifulSoup.

    Args:
        soup (BeautifulSoup): Un objeto BeautifulSoup que contiene el contenido HTML del cual se extraerán las URLs de las imágenes.

    Returns:
        list: Una lista de cadenas de texto que representan las URLs completas de las imágenes extraídas de los elementos con la clase 'product-image'.
    """
    lista_imagen_atrezo = soup.findAll("div",{"class":"product-image"})
    imagenes_atrezo = [f"https://atrezzovazquez.es/{imagen.contents[0].get('src')}" for imagen in lista_imagen_atrezo]
    return imagenes_atrezo

def create_df(webpage):
    """
    Crea un DataFrame de pandas con la información extraída de una página web, que incluye nombre, categoría, sección, descripción, dimensiones y URL de las imágenes.

    Args:
        webpage (str): URL de la página web desde la cual se extraerá la información.

    Returns:
        pd.DataFrame: Un DataFrame con las columnas 'Nombre', 'Categoría', 'Sección', 'Descripción', 'Dimensiones', y 'URL Imágenes' si la solicitud a la URL es exitosa (status code 200).
        None: Si la solicitud a la página falla o no devuelve el código de estado 200.
    """
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
    
