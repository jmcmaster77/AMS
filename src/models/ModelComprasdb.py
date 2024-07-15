from sqlalchemy import Integer
from utils.db import db

class Compras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_p = db.Column(db.Integer)
    productos = db.Column(db.JSON)
    tcompra = db.Column(db.String(10))
    mpago = db.Column(db.String(15))
    pagada = db.Column(db.Boolean)
    totalc = db.Column(db.Float)
    fecha = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean)
    id_u = db.Column(db.Integer)

    def __init__(self, id_p, productos, tcompra, mpago, pagada, totalc, fecha, deleted, id_u):
        self.id_p = id_p
        self.productos = productos
        self.tcompra = tcompra
        self.mpago = mpago
        self.pagada = pagada
        self.totalc = totalc
        self.fecha = fecha
        self.deleted = deleted
        self.id_u = id_u