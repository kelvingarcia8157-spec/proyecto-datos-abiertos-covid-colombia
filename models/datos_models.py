
import json
import os
from datetime import date, datetime

import pyodbc
from dotenv import load_dotenv

load_dotenv()


COLUMNAS_CASO = (
    "id_de_caso",
    "fecha_reporte_web",
    "fecha_de_notificacion",
    "departamento",
    "departamento_nom",
    "ciudad_municipio",
    "ciudad_municipio_nom",
    "edad",
    "unidad_medida",
    "sexo",
    "fuente_tipo_contagio",
    "ubicacion",
    "estado",
    "recuperado",
    "fecha_inicio_sintomas",
    "fecha_diagnostico",
    "fecha_recuperado",
    "tipo_recuperacion",
    "per_etn_",
    "json_original",
)


def conectar_bd():
    """Abre SQL Server usando autenticación Windows o SQL según .env."""
    servidor = os.getenv("DB_SERVER", "").strip()
    base_datos = os.getenv("DB_NAME", "DatosAbiertosColombia").strip()
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server").strip()
    trusted = os.getenv("DB_TRUSTED", "no").strip().lower() in {"1", "true", "yes", "si", "sí"}

    if not servidor or not base_datos or not driver:
        raise ValueError("Configura DB_SERVER, DB_NAME y DB_DRIVER en el archivo .env.")

    partes = [
        f"DRIVER={{{driver}}}",
        f"SERVER={servidor}",
        f"DATABASE={base_datos}",
        "Encrypt=yes",
        "TrustServerCertificate=yes",
    ]
    if trusted:
        partes.append("Trusted_Connection=yes")
    else:
        usuario = os.getenv("DB_USER", "").strip()
        contrasena = os.getenv("DB_PASSWORD", "")
        if not usuario or not contrasena:
            raise ValueError("Con DB_TRUSTED=no debes configurar DB_USER y DB_PASSWORD en .env.")
        partes.extend((f"UID={usuario}", f"PWD={contrasena}"))

    return pyodbc.connect(";".join(partes) + ";", timeout=15)


def _fecha_sql(valor):
    """Convierte fechas ISO de Socrata a date; devuelve None si está vacía/no es válida."""
    if valor in (None, ""):
        return None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    texto = str(valor).strip()
    try:
        return date.fromisoformat(texto[:10])
    except ValueError:
        return None


def _entero_sql(valor):
    if valor in (None, ""):
        return None
    try:
        return int(float(str(valor).strip()))
    except (TypeError, ValueError, OverflowError):
        return None


def _normalizar_caso(registro):
    """Adapta un objeto JSON de gt2j-8ykr a las columnas reales de CasosCovid."""
    identificador = registro.get("id_de_caso")
    if identificador in (None, ""):
        return None
    try:
        identificador = int(str(identificador).strip())
    except (TypeError, ValueError, OverflowError):
        return None

    valores = {
        "id_de_caso": identificador,
        "fecha_reporte_web": _fecha_sql(registro.get("fecha_reporte_web")),
        "fecha_de_notificacion": _fecha_sql(registro.get("fecha_de_notificaci_n")),
        "departamento": registro.get("departamento"),
        "departamento_nom": registro.get("departamento_nom"),
        "ciudad_municipio": registro.get("ciudad_municipio"),
        "ciudad_municipio_nom": registro.get("ciudad_municipio_nom"),
        "edad": _entero_sql(registro.get("edad")),
        "unidad_medida": registro.get("unidad_medida"),
        "sexo": registro.get("sexo"),
        "fuente_tipo_contagio": registro.get("fuente_tipo_contagio"),
        "ubicacion": registro.get("ubicacion"),
        "estado": registro.get("estado"),
        "recuperado": registro.get("recuperado"),
        "fecha_inicio_sintomas": _fecha_sql(registro.get("fecha_inicio_sintomas")),
        "fecha_diagnostico": _fecha_sql(registro.get("fecha_diagnostico")),
        "fecha_recuperado": _fecha_sql(registro.get("fecha_recuperado")),
        "tipo_recuperacion": registro.get("tipo_recuperacion"),
        "per_etn_": registro.get("per_etn_"),
        "json_original": json.dumps(registro, ensure_ascii=False),
    }
    return tuple(valores[columna] for columna in COLUMNAS_CASO)


def guardar_casos(registros):
    """Inserta casos nuevos y cuenta duplicados/omitidos sin sobrescribir existentes."""
    if not isinstance(registros, list):
        raise ValueError("Los registros recibidos deben ser una lista JSON.")

    insertados = duplicados = omitidos = 0
    columnas_sql = ", ".join(f"[{col}]" for col in COLUMNAS_CASO)
    marcadores = ", ".join("?" for _ in COLUMNAS_CASO)
    sql = f"""
        IF NOT EXISTS (
            SELECT 1 FROM dbo.CasosCovid WITH (UPDLOCK, HOLDLOCK)
            WHERE id_de_caso = ?
        )
        BEGIN
            INSERT INTO dbo.CasosCovid ({columnas_sql})
            VALUES ({marcadores});
            SELECT 1 AS insertado;
        END
        ELSE
        BEGIN
            SELECT 0 AS insertado;
        END
    """

    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        for registro in registros:
            if not isinstance(registro, dict):
                omitidos += 1
                continue
            valores = _normalizar_caso(registro)
            if valores is None:
                omitidos += 1
                continue
            cursor.execute(sql, valores[0], *valores)
            resultado = cursor.fetchone()
            if resultado and resultado[0] == 1:
                insertados += 1
            else:
                duplicados += 1
        conexion.commit()
        return {
            "recibidos": len(registros),
            "insertados": insertados,
            "duplicados": duplicados,
            "omitidos": omitidos,
        }
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def consultar_casos(busqueda=""):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        if busqueda:
            consulta = """
                SELECT TOP 200 *
                FROM dbo.CasosCovid
                WHERE CAST(id_de_caso AS VARCHAR(30)) LIKE ?
                   OR ciudad_municipio_nom LIKE ?
                   OR departamento_nom LIKE ?
                ORDER BY id_de_caso DESC
            """
            parametro = f"%{busqueda}%"
            cursor.execute(consulta, parametro, parametro, parametro)
        else:
            cursor.execute("SELECT TOP 200 * FROM dbo.CasosCovid ORDER BY id_de_caso DESC")
        columnas = [col[0] for col in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    finally:
        cursor.close()
        conexion.close()


def obtener_resumen():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT COUNT(*) AS total_casos,
                   AVG(CAST(edad AS FLOAT)) AS edad_promedio,
                   SUM(CASE WHEN recuperado = 'Recuperado' THEN 1 ELSE 0 END) AS total_recuperados
            FROM dbo.CasosCovid
        """)
        fila = cursor.fetchone()
        return {
            "total_casos": fila[0] or 0,
            "edad_promedio": round(fila[1], 1) if fila[1] is not None else 0,
            "total_recuperados": fila[2] or 0,
        }
    finally:
        cursor.close()
        conexion.close()
