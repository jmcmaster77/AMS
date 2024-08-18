from flask import Blueprint, request, redirect, url_for, render_template, flash, send_from_directory
from flask_login import login_required, current_user
from models.ModelVentasdb import Ventas
from models.ModelClientesdb import Clientes
from models.ModelProductosdb import Productos
from models.ModelReversosdb import Reversos
from models.ModelTasadb import Tasa
from datetime import datetime
from utils.db import db
from utils.log import logger
import json
import jinja2
import pdfkit
import os
from config import ipserver

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

        return render_template("gventas/ventas.html", ventas=registros, deleted=True)
    else:
        return render_template("gventas/ventas.html", ventas=registros, deleted=True)


@gventas.route("/rventas", methods=["GET", "POST"])
@login_required
def rventas():
    if request.method == "GET":
        clientes = Clientes.query.all()
        if clientes is not None:
            # buscar productos con contidad > 0 papu 
            productos = Productos.query.filter(Productos.cantidad > 0).all()
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
                # almacenando los datos existente antes de la compra
                cantidaexi = pdata.cantidad

                pdata.cantidad = pdata.cantidad - int(request.form["cantidad"])
                # insertando en la base de datos de reverso el movimiento
                fechar = datetime.now()
                fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                reverso = Reversos(None, pdata.id, cantidaexi, 0,
                                   0, "venta", fechar, current_user.id, True, False)
                db.session.add(reverso)
                db.session.commit()
                totalv = pdata.precio * \
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

                pdata.cantidad = pdata.cantidad - \
                    int(request.form[f"cantidad"+str(x)])

                fechar = datetime.now()
                fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                reverso = Reversos(None, pdata.id, cantidaexi, 0,
                                   0, "compra", fechar, current_user.id, True, False)
                db.session.add(reverso)
                db.session.commit()
                totalv = totalv + (pdata.precio *
                                   int(request.form[f"cantidad"+str(x)]))

        check = request.form.getlist("check[]")
        bolivares = False
        if len(check) != 0:
            # bolivares si
            tasa = db.session.get(Tasa, 1)
            totalv = totalv * tasa.valor
            bolivares = True
            # Bolivares nope
        cliente = Clientes.query.filter_by(
            fullname=request.form['cliente']).first()
        fecha = datetime.now()
        fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
        venta = Ventas(cliente.id, data,
                       request.form["tventa"], request.form["mpago"], bolivares, totalv, fecha, False,  current_user.id)
        db.session.add(venta)
        db.session.commit()
        db.session.query(Reversos).filter(Reversos.registrando == True).update(
            {Reversos.registrando: False, Reversos.id_t: venta.id})
        db.session.commit()

        # finalizando y respondiendo
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                    " | Registro venta id " + str(venta.id))
        flash({'title': "AMS", 'message': "Compra: " +
               "id " + str(venta.id) + " registrado satisfactoriamente"}, 'success')
        return redirect(url_for("gventas.ventas"))


# comprobantes beibi


@gventas.route("/comprobantev/<id>")
@login_required
def comprobantev(id):
    # obteniendo datos de la venta
    ventadata = db.session.get(Ventas, id)
    # obteniendo datos del cliente
    cliente = db.session.get(Clientes, ventadata.id_c)
    fecha = ventadata.fecha.strftime("%d/%m/%Y")
    tasa = db.session.get(Tasa, 1)
    return render_template("comprobantes/comprobantev.html", venta=ventadata, cliente=cliente, fecha=fecha, tasa=tasa)


def creaPdf(ruta_template, ventadata, cliente, fecha, id):
    template_name = ruta_template.split('\\')[-1]
    ruta_template = ruta_template.replace(template_name, '')
    tasa = db.session.get(Tasa, 1)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(template_name)
    rutaimglogo = os.path.abspath(f"src/static/ico/store-svgrepo-com2.svg")
    html = template.render(
        venta=ventadata, cliente=cliente, fecha=fecha, tasa=tasa, ipserver=ipserver)

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
    file_name = f"ams_cv_{id}.pdf"

    rutaarchivo = os.path.abspath(f"src/static/ext/bin/wkhtmltopdf.exe")
    config = pdfkit.configuration(wkhtmltopdf=rutaarchivo)
    ruta_salida = os.path.abspath(f"src/static/pdf/{file_name}")
    cssfile = os.path.abspath(f"src/static/css/comprobante.css")
    pdfkit.from_string(html, ruta_salida, options=options,
                       configuration=config)

    # print(html)
    return file_name


@gventas.route("/comprobantevtpdf/<id>")
@login_required
def comprobantectpdf(id):
    # obteniendo datos de la compra
    ventadata = db.session.get(Ventas, id)
    # obteniendo datos del proveedor
    cliente = db.session.get(Clientes, ventadata.id_c)
    fecha = ventadata.fecha.strftime("%d/%m/%Y")

    ruta_template = "C:\\CODE\\AMS\\src\\templates\\comprobantes\\comprobantepdfv.html"
    # template = "comprobante.html"

    pdf_file = creaPdf(ruta_template, ventadata,
                       cliente, fecha, id)

    return send_from_directory("static/pdf", pdf_file, as_attachment=True)


@gventas.route("/mventa/<id>", methods=["GET", "POST"])
@login_required
def mventa(id):
    dataventa = db.session.get(Ventas, id)
    cliente = db.session.get(Clientes, dataventa.id_c)
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

    if current_user.rol == 0:
        if request.method == "POST":
            itemdb = dataventa.productos
            itemlist = itemdb["productos"]
            for item in itemlist:
                datareverso = Reversos.query.filter(
                    Reversos.id_t == dataventa.id).filter(Reversos.id_p == item["id"])

                for data in datareverso:
                    producto = db.session.get(Productos, item["id"])
                    producto.cantidad = data.cantidad
                    reverso = db.session.get(Reversos, data.id)
                    db.session.delete(reverso)
                    db.session.commit()

                # Reverso cantidad productos realizado
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
                    # almacenando los datos existente antes de la compra
                    cantidaexi = pdata.cantidad

                    pdata.cantidad = pdata.cantidad - \
                        int(request.form["cantidad"])
                    # insertando en la base de datos de reverso el movimiento
                    fechar = datetime.now()
                    fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                    reverso = Reversos(None, pdata.id, cantidaexi, 0,
                                       0, "venta", fechar, current_user.id, True, False)
                    db.session.add(reverso)
                    db.session.commit()
                    totalv = pdata.precio * \
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

                    pdata.cantidad = pdata.cantidad - \
                        int(request.form[f"cantidad"+str(x)])

                    fechar = datetime.now()
                    fechar = fechar.strftime("%Y/%m/%d %H:%M:%S")
                    reverso = Reversos(None, pdata.id, cantidaexi, 0,
                                       0, "compra", fechar, current_user.id, True, False)
                    db.session.add(reverso)
                    db.session.commit()
                    totalv = totalv + (pdata.precio *
                                       int(request.form[f"cantidad"+str(x)]))

            check = request.form.getlist("check[]")

            bolivares = False
            if len(check) != 0:
                # bolivares si
                tasa = db.session.get(Tasa, 1)
                totalv = totalv * tasa.valor
                bolivares = True
                # Bolivares nope
            cliente = Clientes.query.filter_by(
                fullname=request.form['cliente']).first()
            fecha = datetime.now()
            fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
            # venta = Ventas(cliente.id, data,
            #             request.form["tventa"], request.form["mpago"], bolivares, totalv, fecha, False,  current_user.id)
            # db.session.add(venta)
            dataventa.id_c = cliente.id
            dataventa.productos = data
            dataventa.tventa = request.form["tventa"]
            dataventa.mpago = request.form["mpago"]
            dataventa.bolivares = bolivares
            dataventa.totalv = totalv
            dataventa.fecha = fecha
            dataventa.deleted = False
            dataventa.id_u = current_user.id
            db.session.commit()
            db.session.query(Reversos).filter(Reversos.registrando == True).update(
                {Reversos.registrando: False, Reversos.id_t: dataventa.id})
            db.session.commit()

            # finalizando y respondiendo
            logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                        " | Modifico venta id " + str(dataventa.id))
            flash({'title': "AMS", 'message': "Compra: " +
                   "id " + str(dataventa.id) + " modificado satisfactoriamente"}, 'success')
            return redirect(url_for("gventas.ventas"))

        else:

            return render_template("gventas/mventa.html", dataventa=dataventa, datacliente=dataclientes, productos=productos, clien=cliente, jproductos=jproductos)
    else:

        flash({'title': "AMS", 'message': "Un administrador solo puede modificar compras"}, 'error')
        return redirect(url_for("gventas.ventas"))


@gventas.route("/elventa/<id>")
@login_required
def deletedVenta(id):
    if current_user.rol == 0:
        dataventa = db.session.get(Ventas, id)
        itemdb = dataventa.productos
        itemlist = itemdb["productos"]
        # revertir la transaccion en los productos
        for item in itemlist:
            datareverso = Reversos.query.filter(
                Reversos.id_t == dataventa.id).filter(Reversos.id_p == item["id"])
            # print("busqueda reverso", datareverso)
            for data in datareverso:
                # print("datareverso", data.id, data.id_t, data.id_p, data.cantidad, data.costo, data.precio,
                #       data.transaccion, data.fecha, data.id_u, data.registrando, data.reversado)
                producto = db.session.get(Productos, item["id"])
                producto.cantidad = data.cantidad
                reverso = db.session.get(Reversos, data.id)
                db.session.delete(reverso)
                dataventa.deleted = True
                db.session.commit()

        # realizado el reverso continuamos marcando la compra como deleted

        flash({'title': "AMS", 'message': "Venta: " +
               "id " + str(dataventa.id) + " marcada como borrada"}, 'info')
        return redirect(url_for("gventas.ventas"))
    else:
        flash(
            {'title': "AMS", 'message': "Un administrador solo puede eliminar compras"}, 'error')
        return redirect(url_for("gventas.ventas"))
