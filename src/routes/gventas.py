from flask import Blueprint, request, redirect, url_for, render_template, flash, send_from_directory
from flask_login import login_required, current_user
from models.ModelVentasdb import Ventas
from models.ModelClientesdb import Clientes
from models.ModelProductosdb import Productos
from models.ModelReversosdb import Reversos
from datetime import datetime
from utils.db import db
from utils.log import logger
import json
import jinja2
import pdfkit
import os

gventas = Blueprint("gventas", __name__)


@gventas.route("/ventas")
@login_required
def ventas():
    registros = Ventas.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y")

        return render_template("gventas/ventas.html", ventas=registros, deleted=False)
    else:
        return render_template("gventas/ventas.html", ventas=registros, deleted=False)


@gventas.route("/ventas_deleted")
@login_required
def ventas_deleted():
    registros = Ventas.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")

        return render_template("gventas/ventas.html", compras=registros, deleted=True)
    else:
        return render_template("gventas/ventas.html", compras=registros, deleted=True)
