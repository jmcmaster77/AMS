from flask import Blueprint, request, redirect, url_for, render_template, flash, send_from_directory
from flask_login import login_required, current_user
from models.ModelVentasdb import Ventas
from models.ModelClientesdb import Clientes
from models.ModelProductosdb import Productos
from models.ModelPresupuestosdb import Presupuestos
from models.ModelTasadb import Tasa
from datetime import datetime
from utils.db import db
from utils.log import logger
import json
import jinja2
import pdfkit
import os

gpresu = Blueprint("gpresupuestos", __name__)


@gpresu.route("/presupuestos")
@login_required
def presupuestos():
    registros = Presupuestos.query.all()

    busqueda = db.session.query(Presupuestos.id, Clientes.id, Clientes.fullname, Presupuestos.bolivares, Presupuestos.totalp,
                                Presupuestos.productos, Presupuestos.id_u, Presupuestos.deleted, Presupuestos.fecha).filter(Presupuestos.id_c == Clientes.id).all()
    # print(busqueda)
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y")

        return render_template("gpresupuestos/presupuestos.html", presupuestos=registros, deleted=False)
    else:
        return render_template("gpresupuestos/presupuestos.html", presupuestos=registros, deleted=False)


@gpresu.route("/presupuestos_deleted")
@login_required
def presupuestos_deleted():
    registros = Presupuestos.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")

        return render_template("gpresupuestos/presupuestos.html", presupuestos=registros, deleted=True)
    else:
        return render_template("gpresupuestos/presupuestos.html", presupuestos=registros, deleted=True)


@gpresu.route("/rpresupuestos", methods=["GET", "POST"])
@login_required
def rpresupuestos():
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

            return render_template("gpresupuestos/rpresupuesto.html", clientes=clientes, productos=productos, jproductos=jproductos)
        else:
            return render_template("gpresupuestos/rpresupuesto.html", clientes=None)

    else:
        data = {}
        data["productos"] = []

        for x in range(int(request.form["item"])):

            if x == 0:
                # print("aqui llego ")
                # print(request.form)
                pdata = Productos.query.filter_by(
                    nombre=request.form['producto']).first()
                data["productos"].append({
                    "id": pdata.id,
                    "nombre": request.form["producto"],
                    "cantidad": int(request.form["cantidad"]),
                    "precio": pdata.precio
                })
                totalp = pdata.precio * \
                    int(request.form["cantidad"])

            else:
                pdata = Productos.query.filter_by(
                    nombre=request.form[f"producto"+str(x)]).first()
                cantidaexi = pdata.cantidad
                data["productos"].append({
                    "id": pdata.id,
                    "nombre": request.form[f"producto"+str(x)],
                    "cantidad": int(request.form[f"cantidad"+str(x)]),
                    "precio": pdata.precio
                })
                totalp = totalp + (pdata.precio *
                                   int(request.form[f"cantidad"+str(x)]))

        check = request.form.getlist("check[]")
        bolivares = False
        if len(check) != 0:
            # bolivares si
            tasa = db.session.get(Tasa, 1)
            totalp = totalp * tasa.valor
            bolivares = True
            # Bolivares nope
        cliente = Clientes.query.filter_by(
            fullname=request.form['cliente']).first()
        fecha = datetime.now()
        fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
        presupuesto = Presupuestos(
            cliente.id, data, bolivares, totalp, fecha, False, current_user.id)
        db.session.add(presupuesto)
        db.session.commit()

        # finalizando y respondiendo
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                    " | Registro venta id " + str(presupuesto.id))
        flash({'title': "AMS", 'message': "Compra: " +
               "id " + str(presupuesto.id) + " registrado satisfactoriamente"}, 'success')
        return redirect(url_for("gpresupuestos.presupuestos"))

# comprobantes beibi


@gpresu.route("/comprobantep/<id>")
@login_required
def comprobantev(id):
    # obteniendo datos de la venta
    presudata = db.session.get(Presupuestos, id)
    # obteniendo datos del cliente
    cliente = db.session.get(Clientes, presudata.id_c)
    fecha = presudata.fecha.strftime("%d/%m/%Y")
    tasa = db.session.get(Tasa, 1)
    return render_template("comprobantes/presupuesto.html", presupuesto=presudata, cliente=cliente, fecha=fecha, tasa=tasa)


def creaPdf(ruta_template, presudata, cliente, fecha, id):
    template_name = ruta_template.split('\\')[-1]
    ruta_template = ruta_template.replace(template_name, '')
    tasa = db.session.get(Tasa, 1)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(template_name)

    html = template.render(
        presupuesto=presudata, cliente=cliente, fecha=fecha, tasa=tasa)

    options = {
        "page-size": "Letter",
        "margin-top": "0.5in",
        "margin-bottom": "0.5in",
        "margin-right": "0.5in",
        "margin-left": "0.5in",
        "encoding": "UTF-8",
        "enable-local-file-access": None
    }
    # para posible implementacion
    file_name = f"ams_pre_{id}.pdf"

    rutaarchivo = os.path.abspath(f"src/static/ext/bin/wkhtmltopdf.exe")
    config = pdfkit.configuration(wkhtmltopdf=rutaarchivo)
    ruta_salida = os.path.abspath(f"src/static/pdf/{file_name}")
    cssfile = os.path.abspath(f"src/static/css/comprobante.css")
    pdfkit.from_string(html, ruta_salida, options=options,
                       configuration=config)

    # print(html)
    return file_name


@gpresu.route("/comprobanteptpdf/<id>")
@login_required
def comprobantectpdf(id):
    # obteniendo datos de la compra
    presudata = db.session.get(Presupuestos, id)
    # obteniendo datos del proveedor
    cliente = db.session.get(Clientes, presudata.id_c)
    fecha = presudata.fecha.strftime("%d/%m/%Y")

    ruta_template = "C:\\CODE\\AMS\\src\\templates\\comprobantes\\presupuestopdf.html"
    # template = "comprobante.html"

    pdf_file = creaPdf(ruta_template, presudata,
                       cliente, fecha, id)

    return send_from_directory("static/pdf", pdf_file, as_attachment=True)


@gpresu.route("/mpresupuesto/<id>", methods=["GET", "POST"])
@login_required
def mpresupuesto(id):
    datapresu = db.session.get(Presupuestos, id)
    cliente = db.session.get(Clientes, datapresu.id_c)
    dataclientes = Clientes.query.all()
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

    if request.method == "POST":

        data = {}
        data["productos"] = []
        for x in range(int(request.form["item"])):

            if x == 0:

                pdata = Productos.query.filter_by(
                    nombre=request.form['producto']).first()
                data["productos"].append({
                    "id": pdata.id,
                    "nombre": request.form["producto"],
                    "cantidad": int(request.form["cantidad"]),
                    "precio": pdata.precio
                })

                totalp = pdata.precio * \
                    int(request.form["cantidad"])

            else:
                pdata = Productos.query.filter_by(
                    nombre=request.form[f"producto"+str(x)]).first()
                cantidaexi = pdata.cantidad
                data["productos"].append({
                    "id": pdata.id,
                    "nombre": request.form[f"producto"+str(x)],
                    "cantidad": int(request.form[f"cantidad"+str(x)]),
                    "precio": pdata.precio
                })
                totalp = totalp + (pdata.precio *
                                   int(request.form[f"cantidad"+str(x)]))

        check = request.form.getlist("check[]")

        bolivares = False
        if len(check) != 0:
            # bolivares si
            tasa = db.session.get(Tasa, 1)
            totalp = totalp * tasa.valor
            bolivares = True
            # Bolivares nope
        cliente = Clientes.query.filter_by(
            fullname=request.form['cliente']).first()
        fecha = datetime.now()
        fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
        datapresu.id_c = cliente.id
        datapresu.productos = data
        datapresu.bolivares = bolivares
        datapresu.totalp = totalp
        datapresu.fecha = fecha
        datapresu.deleted = False
        datapresu.id_u = current_user.id
        db.session.commit()

        # finalizando y respondiendo
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                    " | Modifico presupuesto id " + str(datapresu.id))
        flash({'title': "AMS", 'message': "Presupuesto: " +
               "id " + str(datapresu.id) + " modificado satisfactoriamente"}, 'success')
        return redirect(url_for("gpresupuestos.presupuestos"))

    else:

        return render_template("gpresupuestos/mpresupuesto.html", datapresu=datapresu, datacliente=dataclientes, productos=productos, clien=cliente, jproductos=jproductos)


@gpresu.route("/elpresupuesto/<id>")
@login_required
def elpresupuesto(id):
    datapresu = db.session.get(Presupuestos, id)

    datapresu.deleted = True
    db.session.commit()

    flash({'title': "AMS", 'message': "Presupuesto: " +
           "id " + str(datapresu.id) + " marcado como borrado"}, 'info')
    return redirect(url_for("gpresupuestos.presupuestos"))


@gpresu.route("/res_presupuesto/<id>")
@login_required
def res_presupuesto(id):
    datapresu = db.session.get(Presupuestos, id)

    datapresu.deleted = False
    db.session.commit()

    flash({'title': "AMS", 'message': "Presupuesto: " +
           "id " + str(datapresu.id) + " restaurado"}, 'info')
    return redirect(url_for("gpresupuestos.presupuestos"))
