

import unittest
from unittest.mock import Mock, patch

from api import api__client


class APIClientTests(unittest.TestCase):
    def test_retorna_lista_json(self):
        respuesta = Mock()
        respuesta.json.return_value = [{"id_de_caso": "1"}]
        with patch.object(api__client.requests, "get", return_value=respuesta) as get:
            resultado = api__client.obtener_casos(1)
        self.assertEqual(resultado, [{"id_de_caso": "1"}])
        respuesta.raise_for_status.assert_called_once()
        self.assertEqual(get.call_args.kwargs["params"]["$limit"], 1)

    def test_rechaza_limite_invalido(self):
        with self.assertRaises(ValueError):
            api__client.obtener_casos(0)

    def test_rechaza_respuesta_que_no_es_lista(self):
        respuesta = Mock()
        respuesta.json.return_value = {"error": "respuesta inválida"}
        with patch.object(api__client.requests, "get", return_value=respuesta):
            with self.assertRaises(ValueError):
                api__client.obtener_casos(1)


if __name__ == "__main__":
    unittest.main()
