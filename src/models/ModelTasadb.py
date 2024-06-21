from utils.db import db

class Tasa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)

    def __init__(self, valor):
        self.valor = valor
