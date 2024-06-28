from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from sqlalchemy import delete
from models.ModelClientesdb import Clientes
from datetime import datetime  # para manejar fechas papu
from utils.db import db
from utils.log import logger


gc = Blueprint("gclientes", __name__)


@gc.route("/clientes")
@login_required
def clientes():
    registros = Clientes.query.all()
    
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
        cliente = Clientes.query.filter_by(documento=request.form['documento']).first()
        # cliente2 = Clientes. experimentando con nuevas formas 
        if cliente is None:

            fecha = datetime.now()
            # fechaf = fecha.strftime("%d/%m/%Y %H:%M:%S")
            fechaf = fecha.strftime("%Y/%m/%d %H:%M:%S")
            clientef = Clientes(request.form['fullname'], request.form['tipod'], request.form['documento'], request.form['numero'] , request.form['email'],
                                request.form['direccion'], fechaf, False, current_user.id)
            print("Cliente F: ", clientef)
            flash({'title': "AMS", 'message': "Cliente: " + request.form['fullname'] + " registrado satisfactoriamente"}, 'success')
            return render_template("gclientes/registroc.html")
        else:
            flash({'title': "AMS", 'message': "Documento: " + request.form['documento'] + " ya esta registrado"}, 'error')
            return render_template("gclientes/registroc.html")
        
