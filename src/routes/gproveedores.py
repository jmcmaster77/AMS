from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from models.ModelProveedoresdb import Proveedores
from datetime import datetime
from utils.db import db
from utils.log import logger


gp = Blueprint("gproveedores", __name__)


@gp.route("/proveedores")
@login_required
def proveedores():
    registros = Proveedores.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")

        return render_template("gproveedores/proveedores.html", proveedores=registros, deleted=False)
    else:
        return render_template("gproveedores/proveedores.html", proveedores=registros, deleted=False)


@gp.route("/proveedores_deleted")
@login_required
def proveedores_deleted():
    registros = Proveedores.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")

        return render_template("gproveedores/proveedores.html", proveedores=registros, deleted=True)
    else:
        return render_template("gproveedores/proveedores.html", proveedores=registros, deleted=True)


@gp.route("/registrarp", methods=["GET", "POST"])
@login_required
def registrar_proveedor():
    if request.method == "GET":

        return render_template("gproveedores/registrop.html")
    else:

        cliente = Proveedores.query.filter_by(
            documento=request.form['documento']).first()
        
        if cliente is None:

            fecha = datetime.now()
            # fechaf = fecha.strftime("%d/%m/%Y %H:%M:%S")
            fechaf = fecha.strftime("%Y/%m/%d %H:%M:%S")
            proveedor = Proveedores(request.form['fullname'], request.form['tipod'], request.form['documento'], request.form['numero'], request.form['email'],
                               request.form['direccion'], fechaf, False, current_user.id)
            db.session.add(proveedor)
            db.session.commit()  # guarda los cambios mosca con esto
            logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                        " | Registro " + request.form['documento'] + " | " + request.form['fullname'])
            flash({'title': "AMS", 'message': "Proveedor: " +
                  request.form['fullname'] + " registrado satisfactoriamente"}, 'success')
            return redirect(url_for("gproveedores.proveedores"))
        else:
            flash({'title': "AMS", 'message': "Documento: " +
                  request.form['documento'] + " ya esta registrado"}, 'error')
            return render_template("gproveedores/registrop.html")


@gp.route("/modificarp/<id>", methods=["GET", "POST"])
@login_required
def modificar_proveedor(id):
    # proveedor = Proveedores.query.get(id)
    proveedor = db.session.get(Proveedores, id)
    if request.method == "POST":
        fecha = datetime.now()
        proveedor.fullname = request.form['fullname']
        proveedor.tipod = request.form['tipod']
        proveedor.documento = request.form['documento']
        proveedor.numero = request.form['numero']
        proveedor.email = request.form['email']
        proveedor.direccion = request.form['direccion']

        # la base de datos acepta el datetime en ese formato papi
        proveedor.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
        proveedor.id_u = current_user.id
        db.session.commit()
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                    " | Modifico " + request.form['documento'] + " | " + request.form['fullname'])
        flash({'title': "AMS", 'message': "Proveedor: " +
               request.form['fullname'] + " modificado"}, 'info')
        return redirect(url_for("gproveedores.proveedores"))
    return render_template("gproveedores/modificarp.html", proveedor=proveedor)


@gp.route("/eliminarp/<id>")
@login_required
def eliminarc(id):
    # proveedor = Proveedores.query.get(id)
    proveedor = db.session.get(Proveedores, id)
    fecha = datetime.now()

    proveedor.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
    proveedor.deleted = True
    proveedor.id_u = current_user.id
    db.session.commit()
    logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                " | Elimino " + proveedor.documento + " | " + proveedor.fullname)
    flash({'title': "AMS", 'message': "Cliente: " +
           proveedor.fullname + " eliminado"}, 'warning')
    return redirect(url_for("gproveedores.proveedores"))


@gp.route("/eliminarpr/<id>")
@login_required
def retaurarp(id):
    if current_user.rol == 0:
        # proveedor = Proveedores.query.get(id)
        proveedor = db.session.get(Proveedores, id)
        fecha = datetime.now()

        proveedor.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
        proveedor.deleted = False
        proveedor.id_u = current_user.id
        db.session.commit()
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                    " | Restauro " + proveedor.documento + " | " + proveedor.fullname)
        flash({'title': "AMS", 'message': "Cliente: " +
               proveedor.fullname + " restaurado"}, 'info')
        return redirect(url_for("gproveedores.proveedores"))
    else:

        flash({'title': "AMS", 'message': "Un administrador solo puede restaurar proveedores"}, 'error')
        return redirect(url_for("gproveedores.proveedores"))
