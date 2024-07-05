from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from models.ModelProductosdb import Productos
from datetime import datetime
from utils.db import db
from utils.log import logger
from werkzeug.utils import secure_filename
import os

gprod = Blueprint("gproductos", __name__)


@gprod.route("/productos")
@login_required
def productos():
    registros = Productos.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")

        return render_template("gproductos/productos.html", productos=registros, deleted=False)
    else:
        return render_template("gproductos/productos.html", productos=registros, deleted=False)


@gprod.route("/productos_deleted")
@login_required
def productos_deleted():
    registros = Productos.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")

        return render_template("gproductos/productos.html", productos=registros, deleted=True)
    else:
        return render_template("gproductos/productos.html", productos=registros, deleted=True)


@gprod.route("/rproducto", methods=["GET", "POST"])
@login_required
def registrar_producto():
    if request.method == "GET":

        return render_template("gproductos/rproducto.html")
    else:
        producto = Productos.query.filter_by(
            codigo=request.form['codigo']).first()

        if producto is None:

            fecha = datetime.now()
            fechaf = fecha.strftime("%Y/%m/%d %H:%M:%S")
            # recuerda borrar el siguiente print papi
            print("datain:", request.form)

            # trabajando con la imagen
            archivo = request.files["imagen"]

            if archivo.filename != "":
                archivo = request.files["imagen"]
                basepath = os.path.dirname(__file__)
                nombrearchivo = secure_filename(archivo.filename)

                # capturando la ext del archivo
                ext = os.path.splitext(nombrearchivo)[1]
                nuevoNombreArchivo = request.form["codigo"] + ext
                rutaarchivo = os.path.abspath(
                    f"src/static/img/productos/" + nuevoNombreArchivo)
                archivo.save(rutaarchivo)
                # creando el registro del producto en la db
                producto = Productos(request.form['codigo'], request.form['nombre'], 0, 0, request.form['porcentaje'], 0, request.form['categoria'],
                                     request.form['descripcion'], nuevoNombreArchivo, fechaf, False, current_user.id)
                db.session.add(producto)
                db.session.commit()  # guarda los cambios mosca con esto
                logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                            " | Registro " + request.form['codigo'] + " | " + request.form['nombre'])
                flash({'title': "AMS", 'message': "Producto: " +
                       request.form['nombre'] + " registrado satisfactoriamente"}, 'success')
                return redirect(url_for("gproductos.productos"))
            else:

                # creando el registro del producto en la db
                producto = Productos(request.form['codigo'], request.form['nombre'], 0, 0, request.form['porcentaje'], 0, request.form['categoria'],
                                     request.form['descripcion'], "box.png", fechaf, False, current_user.id)
                db.session.add(producto)
                db.session.commit()  # guarda los cambios mosca con esto
                logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                            " | Registro " + request.form['codigo'] + " | " + request.form['nombre'])
                flash({'title': "AMS", 'message': "Producto: " +
                       request.form['nombre'] + " registrado satisfactoriamente"}, 'success')
                return redirect(url_for("gproductos.productos"))
        else:
            flash({'title': "AMS", 'message': "Codigo: " +
                  request.form['codigo'] + " ya esta registrado"}, 'error')
            return render_template("gproductos/rproducto.html")
