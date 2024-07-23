from sqlalchemy import Integer
from utils.db import db

class Ventas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_c = db.Column(db.Integer)
    productos = db.Column(db.JSON)
    tventa = db.Column(db.String(10))
    mpago = db.Column(db.String(15))
    totalv = db.Column(db.Float)
    fecha = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean)
    id_u = db.Column(db.Integer)

    def __init__(self, id_p, productos, tcompra, mpago, totalv, fecha, deleted, id_u):
        self.id_c = id_p
        self.productos = productos
        self.tcompra = tcompra
        self.mpago = mpago
        self.totalv = totalv
        self.fecha = fecha
        self.deleted = deleted
        self.id_u = id_u