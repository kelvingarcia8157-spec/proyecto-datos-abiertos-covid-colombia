
"""Comprueba la conexión usando la misma configuración del modelo."""

from models.datos_models import conectar_bd


def main():
    conexion = conectar_bd()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT DB_NAME()")
        resultado = cursor.fetchone()
        print("CONEXIÓN EXITOSA")
        print("Base de datos conectada:", resultado[0])
        cursor.close()
    finally:
        conexion.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("ERROR AL CONECTAR CON SQL SERVER:", error)
        raise SystemExit(1)
