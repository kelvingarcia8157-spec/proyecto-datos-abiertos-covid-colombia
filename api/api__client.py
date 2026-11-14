

import os

import requests
from dotenv import load_dotenv

load_dotenv()

RECURSO_PREDETERMINADO = "gt2j-8ykr"


def obtener_casos(limite=100):
    """Consulta el recurso Socrata y devuelve una lista de diccionarios JSON."""
    if not isinstance(limite, int) or not 1 <= limite <= 50000:
        raise ValueError("El límite debe ser un entero entre 1 y 50000.")
    recurso = os.getenv("API_RESOURCE_ID", RECURSO_PREDETERMINADO).strip()
    url = f"https://www.datos.gov.co/resource/{recurso}.json"
    parametros = {"$limit": limite, "$order": "id_de_caso"}
    respuesta = requests.get(url, params=parametros, timeout=60)
    respuesta.raise_for_status()
    registros = respuesta.json()
    if not isinstance(registros, list):
        raise ValueError("La API no devolvió una lista de registros.")
    return registros
