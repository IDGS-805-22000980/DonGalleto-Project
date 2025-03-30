from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric, Enum

db = SQLAlchemy()

class Galletas(db.Model):
    __tablename__ = 'galletas'
    idGalleta = db.Column(db.Integer, primary_key=True)
    nombreGalleta = db.Column(db.String(50), nullable=False)
    precioPieza = db.Column(Numeric(10,2), nullable=False)
    precioGramo = db.Column(Numeric(10,2), nullable=False)
    precioEmpaque_1kg = db.Column(Numeric(10,2), nullable=False)
    precioEmpaque_700g = db.Column(Numeric(10,2), nullable=False)

    # Relación con InventarioGalletas
    inventario = db.relationship('InventarioGalletas', backref='galleta', lazy=True)

class InventarioGalletas(db.Model):
    __tablename__ = 'inventarioGalletas'
    idInventarioGalletas = db.Column(db.Integer, primary_key=True)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('galletas.idGalleta'), nullable=False)
    cantidadGalleta = db.Column(Numeric(10,2), nullable=False)
