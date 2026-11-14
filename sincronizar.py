

from api.api__client import obtener_casos
from models.datos_models import guardar_casos


def main():
    print("=" * 42)
    print(" SINCRONIZACIÓN DE DATOS COVID-19")
    print("=" * 42)
    registros = obtener_casos(100)
    print("Registros recibidos:", len(registros))
    resultado = guardar_casos(registros)
    print("Registros insertados:", resultado["insertados"])
    print("Registros duplicados:", resultado["duplicados"])
    print("Registros omitidos:", resultado["omitidos"])
    print("Sincronización finalizada.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("ERROR DURANTE LA SINCRONIZACIÓN:", error)
        raise SystemExit(1)
