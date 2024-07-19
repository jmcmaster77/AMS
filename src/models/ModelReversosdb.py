from sqlalchemy import Integer
from utils.db import db

class Reversos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_t = db.Column(db.Integer)
    id_p = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    costo = db.Column(db.Float)
    precio = db.Column(db.Float)
    transaccion = db.Column(db.String(10))
    fecha = db.Column(db.DateTime)
    id_u = db.Column(db.Integer)
    registrando = db.Column(db.Boolean)

    def __init__(self, id_t, id_p, cantidad,costo, precio, transaccion, fecha, id_u, registrando):
        self.id_t = id_t
        self.id_p = id_p
        self.cantidad = cantidad
        self.costo = costo
        self.precio = precio
        self.transaccion = transaccion
        self.fecha = fecha
        self.id_u = id_u
        self.registrando = registrando