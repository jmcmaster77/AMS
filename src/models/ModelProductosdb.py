from sqlalchemy import Integer
from utils.db import db

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(40))
    nombre = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    costo = db.Column(db.Float)
    porcentaje = db.Column(db.Float)
    precio = db.Column(db.Float)
    categoria = db.Column(db.String(30))
    descripcion = db.Column(db.String(150))
    imagen = db.Column(db.String(40))
    fecha = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean)
    id_u = db.Column(db.Integer)

    def __init__(self, codigo, nombre, cantidad, costo, porcentaje, precio, categoria, descripcion, imagen, fecha, deleted, id_u):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.costo = costo
        self.porcentaje = porcentaje
        self.precio = precio
        self.categoria = categoria
        self.descripcion = descripcion
        self.imagen = imagen
        self.fecha = fecha
        self.deleted = deleted
        self.id_u = id_u