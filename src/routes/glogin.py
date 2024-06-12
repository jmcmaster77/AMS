from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, logout_user, UserMixin, current_user
from utils.log import logger
from utils.db import db
from models.ModelUsersdb import Usuarios
from utils.auth import Authenticate

# instanciando ruta en blueprint

glogin = Blueprint("login", __name__)
# base de datos simulada
users = {'jmcmaster77@gmail.com': {'password': '1234'}}


@glogin.route("/")
def tologin():
    logger.info("to login")

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
        print("userdata", userdata.id, userdata.fullname)

        
        if Authenticate.login(userdata, password):

            print("Sesion", userdata.fullname , "succes")

            # login_user(user) # lo estoy realizando en auth.authenticate
            return redirect(url_for("home.home_page"))
        else:
            print("Sesion", userdata.fullname , "failed")
            return redirect(url_for("login.login"))
    else:
        print("Usuario ", username, " no encontrado")

    return redirect(url_for("login.login"))

# ya no lo estoy utlizando


@glogin.route('/protected')
@login_required
def protected():
    return redirect(url_for("home.home_page"))


@glogin.route('/logout')
def logout():
    
    if current_user.is_authenticated:
        logger.info("User id " + str(current_user.id) + " | " + current_user.fullname + " logout")
        logout_user()
        current_app.config['TOASTR_CLOSE_BUTTON'] = 'false'
        current_app.config['TOASTR_TIMEOUT'] = '1500'
        
        flash({'title': "AMS", 'message': "User logout"}, 'info')
        
        return redirect(url_for("login.tologin"))
    else:

        flash({'title': "AMS", 'message': "No user not logged in"}, 'info')
        

    return redirect(url_for("login.tologin"))
