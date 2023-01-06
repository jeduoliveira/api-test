from psutil import cpu_freq
from app import db

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    cpf = db.Column(db.String(255), unique=True)
    tipo = db.Column(db.String(255))
    time_coracao = db.Column(db.String(255))

    def __init__(self, nome, email, cpf, tipo, time_coracao):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.tipo = tipo
        self.time_coracao = time_coracao

    def __repr__(self):
        return '<Cliente %r>' % self.nome
