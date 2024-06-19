from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, current_user
from models.ModelUsersdb import Usuarios
from utils.db import db
from utils.log import logger
from werkzeug.security import generate_password_hash

gu = Blueprint("gusuarios", __name__)


@gu.route("/gusuarios")
def usuarios():
    if current_user.rol == 0:

        resgistros = Usuarios.query.all()
        # print("consulta \n", resgistros[0])
        # for registro in resgistros:
        #     print("id: ", registro.id)
        #     print("username: ", registro.username)
        #     print("fullname: ", registro.fullname)
        #     print("rol: ", registro.rol)

        return render_template("gusuarios/usuarios.html", usuarios=resgistros)
    else:
        flash({'title': "AMS", 'message': "Un administrador solo puede gestionar usuarios"}, 'error')
        return redirect(url_for("home.home_page"))


@gu.route("/registraru", methods=["GET", "POST"])
def registro_usuarios():
    if request.method == "GET":
        # validacion que un usuario ingrese al modulos de gestion de usuario colocando la ruta /registraru
        if current_user.rol == 0:
            return render_template("gusuarios/registrou.html")
        else:
            flash({'title': "AMS", 'message': "Un administrador solo puede gestionar usuarios"}, 'error')
            return redirect(url_for("home.home_page"))
    else:

        # print("Agregando Registros de usuario \n", "Este resgistro papu")
        # print("Datos recibidos:")
        # print("User name: \n", request.form['username'])
        # print("Full name: \n", request.form['fullname'])
        # print("Clave1: \n", request.form['clave1'])
        # print("Clave2: \n", request.form['clave2'])
        # print("rol: \n", request.form['rol'])

        # validar que el username no este registrado

        userdata = Usuarios.query.filter_by(username=request.form['username']).first()

        if userdata == None:
            # validacion de que el username no este registrado, realizada

            if request.form['clave1'] == request.form['clave2']:
                # validar que las claves suministradas coincidan, realizada

                # encriptar la clave
                # generando el objeto usuario
                usuario = Usuarios(request.form['username'], generate_password_hash(request.form['clave2']), request.form['fullname'], request.form['rol'])
                # se lo empujo a la bd

                db.session.add(usuario)
                db.session.commit() # guarda los cambios mosca con esto 

                flash({'title': "AMS", 'message': "Usuario: " + request.form['username'] + " registrado satisfactoriamente"}, 'success')
                return redirect(url_for("gusuarios.usuarios"))
            else:
                flash({'title': "AMS", 'message': "Claves suministradas no coinciden"}, 'error')
                return redirect(url_for("gusuarios.registro_usuarios"))

        else:
            flash({'title': "AMS", 'message': "Usuario ya registrado"}, 'error')
            return redirect(url_for("gusuarios.registro_usuarios"))


@gu.route("/modificaru/<id>", methods=["GET", "POST"])
def modificaru(id):
    
    if current_user.rol == 0:
        # validar que el id 1 solo pueda ser modificado por el mismo
        if current_user.id == 1 and id == "1":
            flash({'title': "AMS", 'message': "se puede editar"}, 'info')
            return redirect(url_for("gusuarios.usuarios"))
        elif current_user != 1 and id == "1":
            flash({'title': "AMS", 'message': "este usuario no puede ser modificado por otro"}, 'info')
            return redirect(url_for("gusuarios.usuarios"))
        elif id != 1:
            flash({'title': "AMS", 'message': "puede modificar el otro usuario"}, 'info')
            return redirect(url_for("gusuarios.usuarios"))
    else:
        flash({'title': "AMS", 'message': "Un administrador solo puede gestionar usuarios"}, 'error')
        return redirect(url_for("home.home_page"))


@gu.route("/eliminaru/<id>", methods=["GET", "POST"])
def eliminaru(id):
    if current_user.rol == 0:
        flash({'title': "AMS", 'message': "en construccion papu"}, 'info')
        return redirect(url_for("gusuarios.usuarios"))
    else:
        flash({'title': "AMS", 'message': "Un administrador solo puede gestionar usuarios"}, 'error')
        return redirect(url_for("home.home_page"))