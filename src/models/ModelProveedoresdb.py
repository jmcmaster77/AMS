from utils.db import db

class Proveedores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(70))
    tipod = db.Column(db.String(5))
    documento = db.Column(db.String(20))
    numero = db.Column(db.String(20))
    email = db.Column(db.String(50))
    direccion = db.Column(db.String(200))
    fecha = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean)
    id_u = db.Column(db.Integer)

    def __init__(self, fullname, tipod, documento, numero, email, direccion, fecha, deleted, id_u):
        self.fullname = fullname
        self.tipod = tipod
        self.documento = documento
        self.numero = numero
        self.email = email
        self.direccion = direccion
        self.fecha = fecha
        self.deleted = deleted
        self.id_u = id_u