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
        return '''
                <form action='login' method='POST'>
                    <input type='text' name='email' id='email' placeholder='email'/>
                    <input type='password' name='password' id='password' placeholder='password'/>
                    <input type='submit' name='submit'/>
                </form>
                '''
    email = request.form['email']

    # consultando a la db 

    consulta = Usuarios.query.all()
    print("consulta", consulta[0].id, consulta[0].fullname)
    if email in users and request.form['password'] == users[email]['password']:
        test = "Jorge"
        logged_user = Authenticate.login(test)
        print("logged_user", logged_user)

        # login_user(user)
        return redirect(url_for("home.home_page"))

    return 'Bad login'

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
