

import os

from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv

from api.api__client import obtener_casos
from models.datos_models import consultar_casos, guardar_casos, obtener_resumen

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave-local-cambiar-en-env")


@app.route("/", methods=["GET"])
def inicio():
    busqueda = request.args.get("buscar", "").strip()
    try:
        casos = consultar_casos(busqueda)
        resumen = obtener_resumen()
        return render_template("index.html", casos=casos, resumen=resumen, busqueda=busqueda)
    except Exception:
        app.logger.exception("No fue posible consultar SQL Server")
        flash("No fue posible consultar la base de datos. Revisa la conexión y la configuración.", "error")
        return render_template(
            "index.html",
            casos=[],
            resumen={"total_casos": 0, "edad_promedio": 0, "total_recuperados": 0},
            busqueda=busqueda,
        ), 500


@app.route("/sincronizar", methods=["POST"])
def sincronizar():
    try:
        registros = obtener_casos(100)
        resultado = guardar_casos(registros)
        flash(
            "Sincronización completada: "
            f"{resultado['insertados']} insertados, "
            f"{resultado['duplicados']} duplicados y "
            f"{resultado['omitidos']} omitidos de {resultado['recibidos']} recibidos.",
            "success",
        )
    except Exception:
        app.logger.exception("Falló la sincronización de datos.gov.co")
        flash("No fue posible sincronizar. Revisa Internet, la API y la conexión con SQL Server.", "error")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"})
