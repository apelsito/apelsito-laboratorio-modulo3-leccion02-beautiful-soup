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
        return None

def convert_to_soup(tosoupcontent):
    soup = BeautifulSoup(tosoupcontent.content, "html.parser")
    return soup