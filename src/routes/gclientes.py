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
    print("Clientes R:", registros)
    return render_template("gclientes/clientes.html", clientes=registros, deleted=False)

@gc.route("/clientes_deleted")
@login_required
def clientes_deleted():
    registros = Clientes.query.all()
    print("Clientes R:", registros)
    return render_template("gclientes/clientes.html", clientes=registros, deleted=True)

@gc.route("/registrarc", methods=["GET", "POST"])
@login_required
def registrar_clientes():
    if request.method == "GET":
    
        return render_template("gclientes/registroc.html")
    else:
        
        return render_template("gclientes/registroc.html")
