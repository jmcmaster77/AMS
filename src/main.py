from flask import Flask, redirect, url_for, flash
import flask_login
from utils.log import logger
from utils.db import db
from models.ModelTasadb import Tasa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_wtf.csrf import CSRFProtect
from routes.glogin import glogin
from routes.home import home
from routes.gusuarios import gu
from routes.gclientes import gc
from routes.gproveedores import gp
from routes.gproductos import gprod
from routes.gcompras import gcomp
from routes.gventas import gventas
from routes.gpresupuestos import gpresu
from config import FLASK_RUN_HOST, FLASK_RUN_PORT, appinfo, storeinfo, creator, sk, DATABASE_CONEXION_URI, ipserver
from utils.auth import Authenticate
from flask_toastr import Toastr

# instancia de la app
app = Flask(__name__)
csrf = CSRFProtect()
# llave de seguridad

app.secret_key = sk

toastr = Toastr()
toastr.init_app(app)

app.config['TOASTR_CLOSE_BUTTON'] = 'false'
app.config['TOASTR_TIMEOUT'] = '1500'

# db conexion
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONEXION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# modificando la configuracion de SQLAlchemy
db.init_app(app)

# modificacion que falla a la primera 
# class Base(DeclarativeBase):
#     pass


# db = SQLAlchemy(app, model_class=Base)


@app.context_processor
def tasa():
    # metodo obsoletro (deprecated) pero funciona
    # tasa = Tasa.query.get(1)
    # es el nuevo metodo pero explota
    tasa = db.session.get(Tasa, 1)
    
    return dict(tasa=tasa)


# login seguridad

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# cargando el usuario que inicio sesion de la webapp


@login_manager.user_loader
def user_loader(id):
    return Authenticate.get_by_id(id)

# manejando en caso de respuesta 401 y 404
# validacion del CSRF token | experimental


def status_400(error):

    flash({'title': "AMS", 'message': "Token experiado"}, 'info')
    return redirect(url_for("login.login"))


def status_401(error):

    flash({'title': "AMS", 'message': "Por favor inicar sesión"}, 'info')
    return redirect(url_for("login.login"))


def status_404(error):

    return redirect(url_for("home.error"))


# registrando Blueprint
app.register_blueprint(glogin)
app.register_blueprint(home)
app.register_blueprint(gu)
app.register_blueprint(gc)
app.register_blueprint(gp)
app.register_blueprint(gprod)
app.register_blueprint(gcomp)
app.register_blueprint(gventas)
app.register_blueprint(gpresu)


if __name__ == '__main__':

    from waitress import serve
    csrf.init_app(app)
    print(appinfo)
    print(storeinfo)
    print(creator)
    print("Ip Server: ", ipserver)

    app.register_error_handler(400, status_400)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)

    logger.info("Servidor running on port: " + str(FLASK_RUN_PORT))
    # ejecutar en produccion
    # serve(app, host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
    # ejecutar en desarrollo
    app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT, debug=True)
