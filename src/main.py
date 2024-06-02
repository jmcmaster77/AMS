from flask import Flask
import flask_login
from utils.log import logger
from utils.db import db
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from routes.glogin import glogin
from routes.home import home
from config import FLASK_RUN_HOST, FLASK_RUN_PORT, appinfo, storeinfo, creator, sk, DATABASE_CONEXION_URI
from utils.auth import Authenticate
from flask_toastr import Toastr 

# instancia de la app
app = Flask(__name__)
csrf = CSRFProtect()
# llave de seguridad

app.secret_key = sk

toastr = Toastr(app)


# db conexion
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONEXION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
db = SQLAlchemy()

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
def user_loader(id):
    return Authenticate.get_by_id(id)


# registrando Blueprint
app.register_blueprint(glogin)
app.register_blueprint(home)

# logger
# logger = logging.getLogger("waitress")
# logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    from waitress import serve
    csrf.init_app(app)
    print(appinfo)
    print(storeinfo)
    print(creator)
    logger.info("Servidor running on port: " + str(FLASK_RUN_PORT))
    serve(app, host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
    # app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
