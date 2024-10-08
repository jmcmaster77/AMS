from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from models.ModelUsersdb import Usuarios
from datetime import datetime # para manejar fechas papu 
from utils.db import db
from utils.log import logger
from werkzeug.security import generate_password_hash

gu = Blueprint("gusuarios", __name__)


@gu.route("/gusuarios")
@login_required
def usuarios():
    if current_user.rol == 0:

        
        # print("consulta \n", resgistros[0])
        # for registro in resgistros:
        #     print("id: ", registro.id)
        #     print("username: ", registro.username)
        #     print("fullname: ", registro.fullname)
        #     print("rol: ", registro.rol)
        # experimentando con la fecha 
        # estableciendo la fecha del sistema 
        # fecha = datetime.now()
        # desde un formulario 
        # dando formato a la fecha 
        # fechan = datetime.strptime(request.form["fechan"], "%d/%m/%Y")
        # otro formato de fecha 
        # fechaf = fecha.strftime("%d/%m/%Y %H:%M:%S")

        # dia = fechan.day
        # mes = fechan.month
        # year = fechan.year
        registros = Usuarios.query.all()
        if registros is not None:
            for registro in registros:
                registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")
            return render_template("gusuarios/usuarios.html", usuarios=registros, deleted=False)
        else:
            return render_template("gusuarios/usuarios.html", usuarios=registros, deleted=False)
    else:
        flash({'title': "AMS", 'message': "Un administrador solo puede gestionar usuarios"}, 'error')
        return redirect(url_for("home.home_page"))

# variable para dar respuesta a mostrar los usuarios borrados papu 
@gu.route("/gusuarios_all")
@login_required
def usuarios_all():
    if current_user.rol == 0:

        registros = Usuarios.query.all()
        if registros is not None:
            for registro in registros:
                registro.fecha = registro.fecha.strftime("%d/%m/%y %H:%M")
            return render_template("gusuarios/usuarios.html", usuarios=registros, deleted=True)
        else:
            return render_template("gusuarios/usuarios.html", usuarios=registros, deleted=True)
    else:
        flash({'title': "AMS", 'message': "Un administrador solo puede gestionar usuarios"}, 'error')
        return redirect(url_for("home.home_page"))


@gu.route("/registraru", methods=["GET", "POST"])
@login_required
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
                fecha = datetime.now()
                # fechaf = fecha.strftime("%d/%m/%Y %H:%M:%S")
                fechaf = fecha.strftime("%Y/%m/%d %H:%M:%S") # la base de datos acepta el datetime en ese formato papi 
                usuario = Usuarios(request.form['username'], generate_password_hash(request.form['clave2']), request.form['fullname'], request.form['rol'], fechaf, False)
                # se lo empujo a la bd
                
                db.session.add(usuario)
                db.session.commit() # guarda los cambios mosca con esto 
                logger.info("User id " + str(current_user.id) + " | " + current_user.fullname + " | usuario " + request.form['username'] + " registrado")
                flash({'title': "AMS", 'message': "Usuario: " + request.form['username'] + " registrado satisfactoriamente"}, 'success')
                return redirect(url_for("gusuarios.usuarios"))
            else:
                flash({'title': "AMS", 'message': "Claves suministradas no coinciden"}, 'error')
                return redirect(url_for("gusuarios.registro_usuarios"))

        else:
            flash({'title': "AMS", 'message': "Usuario ya registrado"}, 'error')
            return redirect(url_for("gusuarios.registro_usuarios"))


@gu.route("/modificaru/<id>", methods=["GET", "POST"])
@login_required
def modificaru(id):

    if current_user.rol == 0:
        # validar que el id 1 solo pueda ser modificado por el mismo
        if current_user.id == 1 and id == "1":
            # metodo obsoleto 
            # userdata = Usuarios.query.get(id)
            # metodo nuevo 
            userdata =  db.session.get(Usuarios, id) 
            if request.method == 'POST':
                # validar que las claves coinciden 
                if request.form['clave1'] == request.form['clave2']:

                    # ahora si almacenando los cambios papu  
                    userdata.username = request.form['username']
                    userdata.fullname = request.form['fullname']
                    userdata.password = generate_password_hash(request.form['clave1'])
                    userdata.rol = request.form['rol']
                    fecha = datetime.now()
                    userdata.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S") # la base de datos acepta el datetime en ese formato papi 
                    db.session.commit()
                    logger.info("User id " + str(current_user.id) + " | " + current_user.fullname + " | usuario " + request.form['username'] + " modificado")
                    flash({'title': "AMS", 'message': "usuario " + request.form['username'] + " modificado"}, 'info')
                    return redirect(url_for("gusuarios.usuarios"))
                else:
                    flash({'title': "AMS", 'message': "Claves suministradas no coinciden"}, 'error')
                    return render_template("gusuarios/modificaru.html", userdata=userdata)
            return render_template("gusuarios/modificaru.html", userdata=userdata)
        # validacion que el usuario con id 1 no sea modificado por otro usuario
        elif current_user.id != 1 and id == "1":
            flash({'title': "AMS", 'message': "este usuario no puede ser modificado"}, 'info')
            return redirect(url_for("gusuarios.usuarios"))
        # validacion que puedan modificar cualquier usuario menos el id 1 
        elif id != "1":  
            # metodo obsoleto 
            # userdata = Usuarios.query.get(id)
            # metodo actual 
            userdata = db.session.get(Usuarios, id) 
            if request.method == 'POST':
                # validacion que el id 4 siempre sea admin 
                if id == "4":
                    
                    userdata.rol = 0
                    # validar que las claves coinciden 
                    if request.form['clave1'] == request.form['clave2']:

                        # ahora si almacenando los cambios papu  
                        userdata.username = request.form['username']
                        userdata.fullname = request.form['fullname']
                        userdata.password = generate_password_hash(request.form['clave1'])
                        fecha = datetime.now()
                        userdata.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S") # la base de datos acepta el datetime en ese formato papi
                        db.session.commit()
                        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname + " | usuario " + request.form['username'] + " modificado")
                        flash({'title': "AMS", 'message': "usuario " + request.form['username'] + " modificado"}, 'info')
                        return redirect(url_for("gusuarios.usuarios"))
                    else:
                        flash({'title': "AMS", 'message': "Claves suministradas no coinciden"}, 'error')
                        return render_template("gusuarios/modificaru.html", userdata=userdata)
                else:     
                # validar que las claves coinciden 
                    if request.form['clave1'] == request.form['clave2']:

                        # ahora si almacenando los cambios papu  
                        userdata.username = request.form['username']
                        userdata.fullname = request.form['fullname']
                        userdata.password = generate_password_hash(request.form['clave1'])
                        userdata.rol = request.form['rol']
                        fecha = datetime.now()
                        userdata.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S") # la base de datos acepta el datetime en ese formato papi
                        db.session.commit()
                        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname + " | usuario " + request.form['username'] + " modificado")
                        flash({'title': "AMS", 'message': "usuario " + request.form['username'] + " modificado"}, 'info')
                        return redirect(url_for("gusuarios.usuarios"))
                    else:
                        flash({'title': "AMS", 'message': "Claves suministradas no coinciden"}, 'error')
                        return render_template("gusuarios/modificaru.html", userdata=userdata)
            return render_template("gusuarios/modificaru.html", userdata=userdata)
    else:
        flash({'title': "AMS", 'message': "Un administrador solo puede gestionar usuarios"}, 'error')
        return redirect(url_for("home.home_page"))


@gu.route("/eliminaru/<id>")
@login_required
def eliminaru(id):
    if current_user.rol == 0:
        if id != "1" and id != "2" and id != "4":
            # metodo obsoleto 
            # userdata = Usuarios.query.get(id)
            # metodo actual 
            userdata = db.session.get(Usuarios, id) 
            logger.warning("User id " + str(current_user.id) + " | " + current_user.fullname + " | usuario id " + id + " | " + userdata.fullname + " eliminado")
            flash({'title': "AMS", 'message': "Usuario con el id " + id + " | " + userdata.fullname + " eliminado"}, 'warning')
            # no se va a borrar se marcara como borrado 
            # db.session.delete(userdata)
            fecha = datetime.now()
            userdata.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S") # la base de datos acepta el datetime en ese formato papi
            userdata.deleted = True
            db.session.commit()
            return redirect(url_for("gusuarios.usuarios"))
        else:
            flash({'title': "AMS", 'message': "Usuario con el id: " + id + " no puede ser eliminado"}, 'info')
            return redirect(url_for("gusuarios.usuarios"))
    else:
        flash({'title': "AMS", 'message': "Un administrador solo puede gestionar usuarios"}, 'error')
        return redirect(url_for("home.home_page"))
    

@gu.route("/eliminarur/<id>")
@login_required
def eliminarur(id):
    if current_user.rol == 0:
        # metodo obsoleto 
        # userdata = Usuarios.query.get(id)
        # metodo actual 
        userdata = db.session.get(Usuarios, id) 
        userdata.deleted = False
        fecha = datetime.now()
        userdata.fecha = fecha.strftime("%Y/%m/%d %H:%M:%S") # la base de datos acepta el datetime en ese formato papi
        db.session.commit()
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname + " | usuario id " + id + " | " + userdata.fullname + " restaurado")
        flash({'title': "AMS", 'message': "Usuario con el id " + id + " | " + userdata.fullname + " restaurado"}, 'success')
        return redirect(url_for("gusuarios.usuarios"))
    else:

        flash({'title': "AMS", 'message': "Un administrador solo puede gestionar usuarios"}, 'error')
        return redirect(url_for("home.home_page"))