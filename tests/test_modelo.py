

import sys
import types
import unittest
from datetime import date
from unittest.mock import patch

try:
    import pyodbc  # noqa: F401
except ImportError:
    sys.modules["pyodbc"] = types.SimpleNamespace(connect=None)

from models import datos_models


class CursorFalso:
    def __init__(self, respuestas):
        self.respuestas = iter(respuestas)
        self.parametros = []
        self.closed = False

    def execute(self, sql, *parametros):
        self.parametros.append(parametros)
        return self

    def fetchone(self):
        return (next(self.respuestas),)

    def close(self):
        self.closed = True


class ConexionFalsa:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def cursor(self):
        return self._cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


class ModeloTests(unittest.TestCase):
    def test_normaliza_campos_reales_de_api(self):
        registro = {
            "id_de_caso": "123",
            "fecha_reporte_web": "2020-03-31T00:00:00.000",
            "fecha_de_notificaci_n": "2020-03-22T00:00:00.000",
            "departamento_nom": "ATLANTICO",
            "ciudad_municipio_nom": "BARRANQUILLA",
            "edad": "25",
            "sexo": "F",
        }
        valores = datos_models._normalizar_caso(registro)
        self.assertEqual(valores[0], 123)
        self.assertEqual(valores[1], date(2020, 3, 31))
        self.assertEqual(valores[2], date(2020, 3, 22))
        self.assertEqual(valores[7], 25)
        self.assertIn('"id_de_caso": "123"', valores[-1])

    def test_omite_registro_sin_identificador(self):
        self.assertIsNone(datos_models._normalizar_caso({"edad": "20"}))

    def test_inserta_nuevo_y_cuenta_duplicado(self):
        cursor = CursorFalso([1, 0])
        conexion = ConexionFalsa(cursor)
        registros = [{"id_de_caso": "10"}, {"id_de_caso": "10"}]
        with patch.object(datos_models, "conectar_bd", return_value=conexion):
            resultado = datos_models.guardar_casos(registros)
        self.assertEqual(resultado["insertados"], 1)
        self.assertEqual(resultado["duplicados"], 1)
        self.assertEqual(resultado["omitidos"], 0)
        self.assertTrue(conexion.committed)
        self.assertTrue(conexion.closed)
        self.assertEqual(len(cursor.parametros), 2)


if __name__ == "__main__":
    unittest.main()
