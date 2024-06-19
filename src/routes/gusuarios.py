from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, current_user
from models.ModelUsersdb import Usuarios
from utils.log import logger

gu = Blueprint("gusuarios", __name__)


@gu.route("/gusuarios", methods=["GET", "POST"])
def usuarios():
    resgistros = Usuarios.query.all()
    # print("consulta \n", resgistros[0])
    # for registro in resgistros:
    #     print("id: ", registro.id)
    #     print("username: ", registro.username)
    #     print("fullname: ", registro.fullname)
    #     print("rol: ", registro.rol)
    
    return render_template("gusuarios/usuarios.html", usuarios = resgistros)
