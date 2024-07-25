from sqlalchemy import Integer
from utils.db import db

class Presupuestos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_c = db.Column(db.Integer)
    productos = db.Column(db.JSON)
    bolivares = db.Column(db.Boolean)
    totalp = db.Column(db.Float)
    fecha = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean)
    id_u = db.Column(db.Integer)

    def __init__(self, id_c, productos, bolivares, totalp, fecha, deleted, id_u):
        self.id_c = id_c
        self.productos = productos
        self.bolivares = bolivares
        self.totalp = totalp
        self.fecha = fecha
        self.deleted = deleted
        self.id_u = id_u