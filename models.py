# Definir as tabelas no banco de dados
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    genero = db.Column(db.String(10))
    endereco = db.relationship('Endereco', backref='user', uselist=False)
    email = db.Column(db.String(100), unique=True)
    telefone = db.Column(db.String(20))
    cpf = db.Column(db.String(14))
    documento = db.Column(db.String(100))
    data_nascimento = db.Column(db.Date)
    senha = db.Column(db.String(100))

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(20))
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
