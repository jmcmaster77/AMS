from flask import Flask
from routes.glogin import glogin

# instancia de la app
app = Flask(__name__)

# registrando Blueprint 
app.register_blueprint(glogin)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
