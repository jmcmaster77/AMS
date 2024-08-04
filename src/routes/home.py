from wsgiref.util import request_uri
from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, current_user
from utils.log import logger
from utils.db import db
from models.ModelTasadb import Tasa
from models.ModelVentasdb import Ventas
from models.ModelClientesdb import Clientes
from models.ModelProveedoresdb import Proveedores
from models.ModelProductosdb import Productos
from sqlalchemy import extract
from datetime import datetime

home = Blueprint("home", __name__)


@home.route('/home')
@login_required
def home_page():
    # tasa = Tasa.query.get(1)
    # flash("Todo OK", 'success')
    # example
    # flash("All OK")
    # flash("All OK", 'success')
    # flash("All Normal", 'info')
    # flash("Not So OK", 'error')
    # flash("So So", 'warning')
    # example custom titles
    # flash("Message", 'Custom Title')
    # flash({'title': "Custom Title", 'message': "Error Message"}, 'error')
    # print ("current app:TOASTR_CLOSE_BUTTON | ", current_app.config.get('TOASTR_CLOSE_BUTTON'))
    # print ("current app.config: ", current_app.config)
    current_app.config['TOASTR_CLOSE_BUTTON'] = 'false'
    current_app.config['TOASTR_TIMEOUT'] = '1500'
    # print ("current app: TOASTR_CLOSE_BUTTON |", current_app.config.get('TOASTR_CLOSE_BUTTON'))

    # ============== recaudacion de datos para el dashboard ==========

    # Ultimas 10 ventas

    # ventasR = db.session.query(Ventas).order_by(Ventas.fecha.desc()).limit(10)

    # Ultimas 10 ventas incluyendo el Nombre del Cliente

    ventasR = db.session.query(Clientes.fullname, Ventas.id, Ventas.productos, Ventas.totalv, Ventas.mpago, Ventas.bolivares).filter(
        Ventas.id_c == Clientes.id).order_by(Ventas.fecha.desc()).limit(10)

    # print("Ventas Recientes:", ventasR)
    # for vr in ventasR:
    #     print("Venta:", vr.id)

    tclientes = Clientes.query.count()
    tproveedores = Proveedores.query.count()
    tproductos = Productos.query.count()

    # res = session.query(Object).filter(
    #   extract('month', Object.created) >= datetime.today().month,
    #   extract('year', Object.created) >= datetime.today().year,
    #   extract('day', Object.created) >= datetime.today().day)
    #  ).all()

    # ===== consult total de ventas diarias =============

    tventasd = db.session.query(Ventas).filter(
        extract('year', Ventas.fecha) == datetime.today().year,
        extract('month', Ventas.fecha) == datetime.today().month,
        extract('day', Ventas.fecha) == datetime.today().day
    ).count()

    # ==== Productos con baja disponibilidad =====

    tproductosdb = db.session.query(Productos).filter(Productos.cantidad <= 10).count()

    productosbd = db.session.query(Productos).filter(Productos.cantidad <= 10).order_by(Productos.fecha.desc()).limit(10)


    return render_template("home.html", fullname=current_user.fullname, ventasr=ventasR, tclientes=tclientes,
                           tproveedores=tproveedores, tproductos=tproductos, tventasd = tventasd,
                            productosbd = productosbd, tproductosdb = tproductosdb)


@home.route("/cambiotasa", methods=["GET", "POST"])
@login_required
def cambiotasa():
    if current_user.rol == 0:
        # tasa = Tasa.query.get(1)
        tasa = db.session.get(Tasa, 1)

        tasa.valor = float(request.form["ntasa"])
        db.session.commit()
        logger.info("User id " + str(current_user.id) + " | " +
                    current_user.fullname + " | tasa de cambio realizada " + str(tasa))
        flash({'title': "AMS", 'message': "Cambio de tasa realizado "}, 'success')
        return redirect("/home")
    else:
        flash({'title': "AMS", 'message': "Un administrador solo puede gestionar cambios de la tasa de cambio del BCV"}, 'error')
        return redirect("/home")


@home.route("/acercade")
@login_required
def acercade():
    return render_template("acerca.html")


@home.route("/error")
@login_required
def error():
    flash({'title': "AMS", 'message': "Recurso no encontrado"}, 'error')
    return render_template("error.html")
