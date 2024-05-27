from utils.db import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(120))
    fullname = db.Column(db.String(50))

    def __init__(self, username, password, fullname):
        self.username = username
        self.password = password
        self.fullname = fullname