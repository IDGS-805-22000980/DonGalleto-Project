from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import datetime

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Nombre de la tabla en la BD
    
    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('Admin', 'Ventas', 'Cocina', 'Cliente', name='roles'), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}, Rol: {self.rol}>'

class Galleta(db.Model):
    __tablename__ = 'Galleta'
    
    id_galleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    precio_por_pieza = db.Column(db.Numeric(10, 2), nullable=False)
    precio_por_gramo = db.Column(db.Numeric(10, 2), nullable=False)
    cantidadGalletas = db.Column(db.Integer, nullable=False)


class Receta(db.Model):
    __tablename__ = 'recetas'
    
    idReceta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreReceta = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255), nullable=False)
    cantidadGalletaProducida = db.Column(db.Integer, nullable=False)
    diasCaducidad = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Receta {self.nombreReceta}>'

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    
    idIngrediente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreIngrediente = db.Column(db.String(100), nullable=False, unique=True)
    unidadMedida = db.Column(db.Enum('gramo', 'kilogramo', 'litro', 'mililitro', 'pieza', 'bulto', name='unidades_medida'), nullable=False)
    cantidadInventario = db.Column(Numeric(10,2), nullable=False)
    fechaCaducidad = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f'<Ingrediente {self.nombreIngrediente}>'

class IngredienteReceta(db.Model):
    __tablename__ = 'ingredientesReceta'
    
    idIngredientesReceta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idReceta = db.Column(db.Integer, db.ForeignKey('recetas.idReceta'), nullable=False)
    idIngrediente = db.Column(db.Integer, db.ForeignKey('ingredientes.idIngrediente'), nullable=False)
    cantidadNecesaria = db.Column(Numeric(10,2), nullable=False)
    
    receta = db.relationship('Receta', backref='ingredientes_asociados')
    ingrediente = db.relationship('Ingrediente')

class InventarioGalletas(db.Model):
    __tablename__ = 'inventarioGalletas'
    
    idGalleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idReceta = db.Column(db.Integer, db.ForeignKey('recetas.idReceta'), nullable=False)
    fechaProduccion = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    fechaCaducidad = db.Column(db.Date, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.Enum('Pieza', 'Paquete 1kg', 'Paquete 700g', 'Kilogramos', 'Gramos', name='tipos_galleta'), nullable=False)
    
    receta = db.relationship('Receta', backref='galletas')
    
    def __repr__(self):
        return f'<Galleta {self.idGalleta} - Receta {self.idReceta}>'

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    idPedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    fechaPedido = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    estado = db.Column(db.Enum('Pendiente', 'En proceso', 'Listo para recoger', 'Entregado', 'Cancelado'), nullable=False, default='Pendiente')
    direccionEntrega = db.Column(db.String(255), nullable=False)
    telefonoContacto = db.Column(db.String(20), nullable=False)
    notas = db.Column(db.Text)
    total = db.Column(Numeric(10,2), nullable=False)
    
    usuario = db.relationship('Usuario', backref='pedidos')
    detalles = db.relationship('DetallePedido', backref='pedido', cascade='all, delete-orphan')

# En models/models.py, cambiar la relación en DetallePedido:
class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'
    
    idDetallePedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idPedido = db.Column(db.Integer, db.ForeignKey('pedidos.idPedido'), nullable=False)
    idGalleta = db.Column(db.Integer, db.ForeignKey('Galleta.id_galleta'), nullable=False)  # Cambiado a Galleta
    cantidad = db.Column(db.Integer, nullable=False)
    precioUnitario = db.Column(Numeric(10,2), nullable=False)
    subtotal = db.Column(Numeric(10,2), nullable=False)
    
    galleta = db.relationship('Galleta')  # Relación con Galleta en lugar de InventarioGalletas
    idGalletaInventario = db.Column(db.Integer, db.ForeignKey('inventarioGalletas.idGalleta'))


class SeguimientoPedido(db.Model):
    __tablename__ = 'seguimiento_pedidos'
    
    idSeguimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idPedido = db.Column(db.Integer, db.ForeignKey('pedidos.idPedido'), nullable=False)
    estadoAnterior = db.Column(db.Enum('Pendiente', 'En proceso', 'Listo para recoger', 'Entregado', 'Cancelado'))
    estadoNuevo = db.Column(db.Enum('Pendiente', 'En proceso', 'Listo para recoger', 'Entregado', 'Cancelado'), nullable=False)
    fechaCambio = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    idUsuarioCambio = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'))
    comentarios = db.Column(db.Text)
    
    usuario = db.relationship('Usuario')