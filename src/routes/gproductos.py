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
           
            # trabajando con la imagen
            archivo = request.files["imagen"]

            if archivo.filename != "":
                
                
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
        

@gprod.route("/mproducto/<id>", methods=["GET", "POST"])
@login_required
def modificar_producto(id):
    producto = Productos.query.get(id)
    if request.method == "POST":
        # check para validar si mantiene la imagen de producto
        check = request.form.getlist("check[]")

        if len(check) != 0:
            if producto.precio != 0:
                fecha = datetime.now()
                # reajusta el precio del producto papi
                producto.precio =  producto.costo * ((float(request.form['porcentaje'])/100)+1)  # float(request.form[f"costo"+str(x)]) * ((pdata.porcentaje/100)+1)
                
                producto.codigo = request.form['codigo']
                producto.nombre = request.form['nombre']
                producto.porcentaje = request.form['porcentaje']
                producto.categoria = request.form['categoria']
                producto.descripcion = request.form['descripcion']
                
                # la base de datos acepta el datetime en ese formato papi
                producto.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
                producto.id_u = current_user.id
                db.session.commit()
                logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                            " | Modifico " + request.form['codigo'] + " | " + request.form['nombre'])
                flash({'title': "AMS", 'message': "Producto: " +
                        request.form['nombre'] + " Modificado satisfactoriamente"}, 'success')

            return redirect(url_for("gproductos.productos"))

        else:
            
            archivo = request.files["imagen"]
            if archivo.filename != "":
                if producto.precio != 0:
                    # reajusta el precio del producto papi
                    producto.precio =  producto.costo * ((float(request.form['porcentaje'])/100)+1)
                    
                    nombrearchivo = secure_filename(archivo.filename)
                    # capturando la ext del archivo
                    ext = os.path.splitext(nombrearchivo)[1]
                    nuevoNombreArchivo = request.form["codigo"] + ext
                    rutaarchivo = os.path.abspath(
                        f"src/static/img/productos/" + nuevoNombreArchivo)
                    archivo.save(rutaarchivo)

                    fecha = datetime.now()
                    producto.codigo = request.form['codigo']
                    producto.nombre = request.form['nombre']
                    producto.porcentaje = request.form['porcentaje']
                    producto.categoria = request.form['categoria']
                    producto.descripcion = request.form['descripcion']
                    producto.imagen = nuevoNombreArchivo
                    # la base de datos acepta el datetime en ese formato papi
                    producto.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
                    producto.id_u = current_user.id
                    db.session.commit()
                    logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                                " | Modifico " + request.form['codigo'] + " | " + request.form['nombre'])
                    flash({'title': "AMS", 'message': "Producto: " +
                            request.form['nombre'] + " Modificado satisfactoriamente"}, 'success')
                return redirect(url_for("gproductos.productos"))
            else:
                if producto.precio != 0:
                    # reajusta el precio del producto papi
                    producto.precio =  producto.costo * ((float(request.form['porcentaje'])/100)+1)
                    fecha = datetime.now()
                    producto.codigo = request.form['codigo']
                    producto.nombre = request.form['nombre']
                    producto.porcentaje = request.form['porcentaje']
                    producto.categoria = request.form['categoria']
                    producto.descripcion = request.form['descripcion']
                    producto.imagen = "box.png"
                    # la base de datos acepta el datetime en ese formato papi
                    producto.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
                    producto.id_u = current_user.id
                    db.session.commit()
                    logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                                " | Modifico " + request.form['codigo'] + " | " + request.form['nombre'])
                    flash({'title': "AMS", 'message': "Producto: " +
                            request.form['nombre'] + " Modificado satisfactoriamente"}, 'success')

                return redirect(url_for("gproductos.productos"))
    return render_template("gproductos/mproducto.html", producto=producto)


@gprod.route("/eproducto/<id>")
@login_required
def eliminar_productos(id):
    producto = Productos.query.get(id)
    fecha = datetime.now()
    
    producto.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
    producto.deleted = True
    producto.id_u = current_user.id
    db.session.commit()
    logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                " | Elimino " + producto.codigo + " | " + producto.nombre)
    flash({'title': "AMS", 'message': "Producto: " +
           producto.nombre + " eliminado"}, 'warning')
    return redirect(url_for("gproductos.productos"))


@gprod.route("/rproducto/<id>")
@login_required
def retaurar_productos(id):
    if current_user.rol == 0:
        producto = Productos.query.get(id)
        fecha = datetime.now()

        producto.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
        producto.deleted = False
        producto.id_u = current_user.id
        db.session.commit()
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                    " | Restauro " + producto.codigo + " | " + producto.nombre)
        flash({'title': "AMS", 'message': "Producto: " +
               producto.nombre + " restaurado"}, 'info')
        return redirect(url_for("gproductos.productos"))
    else:

        flash({'title': "AMS", 'message': "Un administrador solo puede restaurar productos"}, 'error')
        return redirect(url_for("gproductos.productos"))