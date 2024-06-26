from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, logout_user, UserMixin, current_user
from sqlalchemy import true
from utils.log import logger
from models.ModelUsersdb import Usuarios
from models.ModelTasadb import Tasa
from utils.auth import Authenticate

# instanciando ruta en blueprint

glogin = Blueprint("login", __name__)


@glogin.route("/")
def tologin():
    if current_user.is_authenticated:
        return redirect(url_for("home.home_page"))
    else:
        
        return redirect(url_for("login.login"))


@glogin.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template("auth/login.html")

    username = request.form['username']
    password = request.form['password']

    # consultando a la db

    # consulta = Usuarios.query.all()

    userdata = Usuarios.query.filter_by(username=username).first()

    if userdata != None:

        if Authenticate.login(userdata, password):

            # login_user(user) # lo estoy realizando en auth.authenticate
            if userdata.deleted == True:
                logger.error("User id " + str(current_user.id) + " | " + current_user.fullname + " | login user deleted")
                flash({'title': "AMS", 'message': "Usuario inhabilitado"}, 'error')
                logout_user()
                return redirect(url_for("login.login"))
            else:
                logger.info("User id " + str(current_user.id) + " | " + current_user.fullname + " | login")
                flash({'title': "AMS", 'message': "Bienvenido " + current_user.fullname}, 'success')
                
                return redirect(url_for("home.home_page"))
        else:
            # no puedes colocar attributos del usuarios si no esta authenticate 
            logger.warning("User id " + username + " | error clave")
            flash({'title': "AMS", 'message': "Error clave"}, 'error')
            return redirect(url_for("login.login"))
    else:
        
        flash({'title': "AMS", 'message': "no encontrado"}, 'error')
        logger.error("Usuario " + username + " no encontrado error login")
        
    return redirect(url_for("login.login"))

# ya no lo estoy utlizando


@glogin.route('/protected')
@login_required
def protected():
    return redirect(url_for("home.home_page"))


@glogin.route('/logout')
def logout():

    if current_user.is_authenticated:
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname + " | logout")
        logout_user()
        current_app.config['TOASTR_CLOSE_BUTTON'] = 'false'
        current_app.config['TOASTR_TIMEOUT'] = '1500'

        flash({'title': "AMS", 'message': "User logout"}, 'info')

        return redirect(url_for("login.tologin"))
    else:

        flash({'title': "AMS", 'message': "No user not logged in"}, 'info')

    return redirect(url_for("login.tologin"))
