import requests
import json


URL = "https://www.datos.gov.co/resource/gt2j-8ykr.json"


parametros = {
    "$limit": 5
}

print("====================================")
print(" PRUEBA DE API - CASOS COVID-19")
print("====================================")

try:
   
    respuesta = requests.get(
        URL,
        params=parametros,
        timeout=30
    )

    print("Código HTTP:", respuesta.status_code)

    
    respuesta.raise_for_status()


    registros = respuesta.json()

    if not isinstance(registros, list):
        raise ValueError("La respuesta no tiene formato de lista JSON.")

    print("Cantidad recibida:", len(registros))

    if registros:
        print("\nPrimer registro recibido:")
        print(
            json.dumps(
                registros[0],
                indent=4,
                ensure_ascii=False
            )
        )

        print("\nCampos encontrados:")

        for campo in registros[0].keys():
            print("-", campo)

    else:
        print("La API no devolvió registros.")

except requests.exceptions.RequestException as error:
    print("ERROR DE CONEXIÓN O API:")
    print(error)

except ValueError as error:
    print("ERROR AL PROCESAR LOS DATOS:")
    print(error)
