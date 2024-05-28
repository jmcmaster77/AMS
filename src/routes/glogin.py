from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, login_user, logout_user, UserMixin, current_user
from utils.log import logger


# instanciando ruta en blueprint

glogin = Blueprint("login", __name__)
# base de datos simulada
users = {'jmcmaster77@gmail.com': {'password': '1234'}}

# formateando los datos de la base de datos


class User(UserMixin):
    pass


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

    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        login_user(user)
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
