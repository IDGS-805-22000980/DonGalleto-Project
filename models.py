from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric

db = SQLAlchemy()

class Galleta(db.Model):
    __tablename__ = 'Galleta'
    
    id_galleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    precio_por_pieza = db.Column(db.Numeric(10, 2), nullable=False)
    precio_por_gramo = db.Column(db.Numeric(10, 2), nullable=False)
    cantidadGalletas = db.Column(db.Integer, nullable=False)