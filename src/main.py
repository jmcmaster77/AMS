from flask import Flask
import flask_login
import logging
from routes.glogin import glogin
from routes.home import home
from config import FLASK_RUN_HOST, FLASK_RUN_PORT, appinfo, creator, sk, DATABASE_CONEXION_URI

# instancia de la app
app = Flask(__name__)

# llave de seguridad

app.secret_key = sk


# db conexion
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONEXION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# login seguridad

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# eso va para models


class User(flask_login.UserMixin):
    pass


# base de datos simulada se va cuando sea una consulta de verdad
users = {'jmcmaster77@gmail.com': {'password': '1234'}}

# cargando el usuario que inicio sesion de la webapp


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user


# registrando Blueprint
app.register_blueprint(glogin)
app.register_blueprint(home)

# logger
logger = logging.getLogger("waitress")
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    from waitress import serve
    print(appinfo)
    print(creator)
    print("Servidor running on port: ", FLASK_RUN_PORT)
    serve(app, host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
    # app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
