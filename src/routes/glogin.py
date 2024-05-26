from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, login_user, logout_user, UserMixin, current_user


# instanciando ruta en blueprint

glogin = Blueprint("login", __name__)

users = {'jmcmaster77@gmail.com': {'password': '1234'}}


class User(UserMixin):
    pass


@glogin.route("/")
def index():
    print("solicitud get a /")
    return redirect(url_for("login.login"))


@glogin.route('/login', methods=['GET', 'POST'])
def login():
    print("Login get")
    if request.method == 'GET':
        return '''
                <form action='login' method='POST'>
                    <input type='text' name='email' id='email' placeholder='email'/>
                    <input type='password' name='password' id='password' placeholder='password'/>
                    <input type='submit' name='submit'/>
                </form>
                '''
    email = request.form['email']
    print("userfdb", users)
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        print("user", user.id)  # comentar
        print("pass")  # comentar
        login_user(user)
        return redirect(url_for("login.protected"))

    return 'Bad login'


@glogin.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id

@glogin.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

