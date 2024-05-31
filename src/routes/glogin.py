from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, login_user, logout_user, UserMixin, current_user
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
    print("username: " + username)
    id = 1
    consulta = Usuarios.query.filter_by(username=username).first()
    print("Consulta", consulta) 
    # print("consulta", consulta[0].id, consulta[0].fullname)
    if consulta != None:

        test = "Jorge"
        if Authenticate.login(test):

            print("Sesion", test, "succes")

            # login_user(user)
            return redirect(url_for("home.home_page"))
    else:
        print("Usuario ", username ," no encontrado")

    return redirect(url_for("login.login"))

# ya no lo estoy utlizando


@glogin.route('/protected')
@login_required
def protected():
    return redirect(url_for("home.home_page"))


@glogin.route('/logout')
def logout():
    logger.info("User id " + current_user.id + " logout")
    logout_user()

    return 'Logged out'
