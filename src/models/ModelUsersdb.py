from utils.db import db

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(240))
    fullname = db.Column(db.String(50))
    rol = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean)

    def __init__(self, username, password, fullname, rol, fecha, deleted):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.rol = rol
        self.fecha = fecha
        self.deleted = deleted
