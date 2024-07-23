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


@gventas.route("/rventas", methods=["GET", "POST"])
@login_required
def rventas():
    if request.method == "GET":
        clientes = Clientes.query.all()
        if clientes is not None:
            productos = Productos.query.all()
            jproductos = {}
            jproductos["productos"] = []      
            for producto in productos:
                jproductos["productos"].append({
                        "id": producto.id,
                        "nombre": producto.nombre,
                        "cantidad": producto.cantidad,
                        "precio": producto.precio
                })
            jproductos = json.dumps(jproductos, indent=4)
            jpl = json.loads(jproductos)
                
    
            return render_template("gventas/rventas.html", clientes=clientes, productos=productos, jproductos=jproductos)
        else:
            return render_template("gventas/rventas.html", clientes=None)
    else:
        check = request.form.getlist("check[]")
        if len(check) != 0:
            # bolivares si 
            logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                        " | Registro venta id " + str(1))
            flash({'title': "AMS", 'message': "Compra: " +
                   "id " + str(1) + " registrado satisfactoriamente"}, 'success')
            # logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
            #             " | Registro venta id " + str(venta.id))
            # flash({'title': "AMS", 'message': "Compra: " +
            #        "id " + str(venta.id) + " registrado satisfactoriamente"}, 'success')
        else:
            # bolivares no

            logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                        " | Registro venta id " + str(1))
            flash({'title': "AMS", 'message': "Compra: " +
                   "id " + str(1) + " registrado satisfactoriamente"}, 'success')
            # logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
            #             " | Registro venta id " + str(venta.id))
            # flash({'title': "AMS", 'message': "Compra: " +
            #        "id " + str(venta.id) + " registrado satisfactoriamente"}, 'success')
        return render_template("gventas/ventas.html")
