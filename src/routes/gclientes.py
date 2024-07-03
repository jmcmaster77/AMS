from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from sqlalchemy import delete
from models.ModelClientesdb import Clientes
from datetime import datetime  # para manejar fechas papu
from routes.glogin import login
from utils.db import db
from utils.log import logger


gc = Blueprint("gclientes", __name__)


@gc.route("/clientes")
@login_required
def clientes():
    registros = Clientes.query.all()
    if registros is not None:
        for registro in registros:
            registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")

        return render_template("gclientes/clientes.html", clientes=registros, deleted=False)
    else:
        return render_template("gclientes/clientes.html", clientes=registros, deleted=False)


@gc.route("/clientes_deleted")
@login_required
def clientes_deleted():
    registros = Clientes.query.all()

    return render_template("gclientes/clientes.html", clientes=registros, deleted=True)


@gc.route("/registrarc", methods=["GET", "POST"])
@login_required
def registrar_clientes():
    if request.method == "GET":

        return render_template("gclientes/registroc.html")
    else:

        print("Datos cliente del form: ", request.form)
        cliente = Clientes.query.filter_by(
            documento=request.form['documento']).first()
        # cliente2 = Clientes. experimentando con nuevas formas
        if cliente is None:

            fecha = datetime.now()
            # fechaf = fecha.strftime("%d/%m/%Y %H:%M:%S")
            fechaf = fecha.strftime("%Y/%m/%d %H:%M:%S")
            cliente = Clientes(request.form['fullname'], request.form['tipod'], request.form['documento'], request.form['numero'], request.form['email'],
                               request.form['direccion'], fechaf, False, current_user.id)
            db.session.add(cliente)
            db.session.commit()  # guarda los cambios mosca con esto
            logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                        " | Registro " + request.form['documento'] + " | " + request.form['fullname'])
            flash({'title': "AMS", 'message': "Cliente: " +
                  request.form['fullname'] + " registrado satisfactoriamente"}, 'success')
            return redirect(url_for("gclientes.clientes"))
        else:
            flash({'title': "AMS", 'message': "Documento: " +
                  request.form['documento'] + " ya esta registrado"}, 'error')
            return render_template("gclientes/registroc.html")


@gc.route("/modificarc/<id>", methods=["GET", "POST"])
@login_required
def modificar_cliente(id):
    cliente_data = Clientes.query.get(id)
    if request.method == "POST":
        fecha = datetime.now()
        cliente_data.fullname = request.form['fullname']
        cliente_data.tipod = request.form['tipod']
        cliente_data.documento = request.form['documento']
        cliente_data.numero = request.form['numero']
        cliente_data.email = request.form['email']
        cliente_data.direccion = request.form['direccion']

        # la base de datos acepta el datetime en ese formato papi
        cliente_data.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
        cliente_data.id_u = current_user.id
        db.session.commit()
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                    " | Modifico " + request.form['documento'] + " | " + request.form['fullname'])
        flash({'title': "AMS", 'message': "Cliente: " +
               request.form['fullname'] + " modificado"}, 'info')
        return redirect(url_for("gclientes.clientes"))
    return render_template("gclientes/modificarc.html", cliente=cliente_data)


@gc.route("/eliminarc/<id>")
@login_required
def eliminarc(id):
    cliente_data = Clientes.query.get(id)
    fecha = datetime.now()

    cliente_data.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
    cliente_data.deleted = True
    cliente_data.id_u = current_user.id
    db.session.commit()
    logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
                " | Elimino " + cliente_data.documento + " | " + cliente_data.fullname)
    flash({'title': "AMS", 'message': "Cliente: " +
           cliente_data.fullname + " eliminado"}, 'warning')
    return redirect(url_for("gclientes.clientes"))


@gc.route("/eliminarcr/<id>")
@login_required
def retaurarc(id):
    if current_user.rol == 0:
        cliente_data = Clientes.query.get(id)
        fecha = datetime.now()

        cliente_data.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
        cliente_data.deleted = False
        cliente_data.id_u = current_user.id
        db.session.commit()
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname +
            " | Restauro " + cliente_data.documento + " | " + cliente_data.fullname)
        flash({'title': "AMS", 'message': "Cliente: " +
                cliente_data.fullname + " restaurado"}, 'info')
        return redirect(url_for("gclientes.clientes"))
    else:

        flash({'title': "AMS", 'message': "Un administrador solo puede restaurar clientes"}, 'error')
        return redirect(url_for("gclientes.clientes"))