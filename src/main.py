from flask import Flask
from routes.glogin import glogin
from config import FLASK_RUN_HOST, FLASK_RUN_PORT, creator

# instancia de la app
app = Flask(__name__)

# registrando Blueprint 
app.register_blueprint(glogin)

if __name__ == '__main__':
    app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
