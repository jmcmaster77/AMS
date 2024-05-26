from flask import Flask
import flask_login, logging
from routes.glogin import glogin
from config import FLASK_RUN_HOST, FLASK_RUN_PORT, appinfo, creator, sk

# instancia de la app
app = Flask(__name__)

# llave de seguridad 

app.secret_key = sk

# login seguridad

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

users = {'jmcmaster77@gmail.com': {'password': '1234'}}

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    print("email", email)
    user = User()
    user.id = email
    return user

# registrando Blueprint
app.register_blueprint(glogin)

# logger 
logger = logging.getLogger("waitress")
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    from waitress import serve
    print(appinfo)
    print(creator)
    print("Servidor running on port: ", FLASK_RUN_PORT)
    serve(app, host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
    # app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
    
