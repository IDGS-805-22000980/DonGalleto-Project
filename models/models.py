from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric

db = SQLAlchemy()

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('Admin', 'Ventas', 'Cocina', 'Cliente', name='roles'), nullable=False)
    
    def __repr__(self):
        return f'<Usuario {self.nombre}, Rol: {self.rol}>'

# Modelo de Insumos
class Insumo(db.Model):
    __tablename__ = 'insumos'
    id_insumo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    unidad = db.Column(db.Enum('gramo', 'kilogramo', 'litro', 'mililitro', 'pieza', 'bulto', name='unidades_insumo'), nullable=False)
    cantidad_disponible = db.Column(Numeric(10, 2), nullable=False, default=0)
    merma = db.Column(Numeric(5, 2), nullable=False, default=0)
    fechaCaducidad = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f'<Insumo {self.nombre} ({self.cantidad_disponible} {self.unidad})>'

# Modelo de Recetas
class Receta(db.Model):
    __tablename__ = 'recetas'
    idReceta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreReceta = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    cantidadGalletaProducida = db.Column(db.Integer, nullable=False)
    diasCaducidad = db.Column(db.Integer, nullable=False)

# Modelo de Ingredientes
class Ingredientes(db.Model):
    __tablename__ = 'ingredientes'
    idIngrediente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreIngrediente = db.Column(db.String(100), nullable=False)
    cantidadInventario = db.Column(db.Integer, nullable=False)
    unidadMedida = db.Column(db.Enum('gramo', 'kilogramo', 'litro', 'mililitro', 'pieza', 'bulto', name='unidades_ingrediente'), nullable=False)
    fechaCaducidad = db.Column(db.Date, nullable=False)

# Modelo de Ingrediente Receta
class IngredienteReceta(db.Model):
    __tablename__ = 'ingredienteReceta'
    idIngredienteReceta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idReceta = db.Column(db.Integer, db.ForeignKey('recetas.idReceta', ondelete="CASCADE"), nullable=False)
    idIngrediente = db.Column(db.Integer, db.ForeignKey('ingredientes.idIngrediente', ondelete="CASCADE"), nullable=False)
    cantidadNecesaria = db.Column(db.Integer, nullable=False)
    Receta = db.relationship('Receta', backref=db.backref('ingredientes', cascade="all, delete-orphan"))
    Ingrediente = db.relationship('Ingredientes', backref=db.backref('recetas', cascade="all, delete-orphan"))

# Modelo de Produccion
class Produccion(db.Model):
    __tablename__ = 'produccion'
    idProduccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idReceta = db.Column(db.Integer, db.ForeignKey('recetas.idReceta', ondelete="CASCADE"), nullable=False)
    fechaCaducidad = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario', ondelete="CASCADE"), nullable=False)
    fechaProduccion = db.Column(db.Date, nullable=False)
    Receta = db.relationship('Receta', backref=db.backref('produccion', cascade="all, delete-orphan"))

# Modelo de Inventario Galletas
class InventarioGalletas(db.Model):
    __tablename__ = 'inventarioGalletas'
    idGalleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idReceta = db.Column(db.Integer, db.ForeignKey('recetas.idReceta', ondelete="CASCADE"), nullable=False)
    fechaProduccion = db.Column(db.Date, nullable=False)
    fechaCaducidad = db.Column(db.Date, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.Enum('Pieza', 'Paquete 1kg', 'Paquete 700g', 'Kilogramos', 'Gramos', name='tipo_galleta'), nullable=False)
    receta = db.relationship('Receta', backref=db.backref('inventario', cascade="all, delete-orphan"))

# Modelo de Ventas
class Ventas(db.Model):
    __tablename__ = 'ventas'
    idVenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario', ondelete="CASCADE"), nullable=False)
    fechaVenta = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    Usuario = db.relationship('Usuario', backref=db.backref('ventas', cascade="all, delete-orphan"))

# Modelo Inventario
class Inventario(db.Model):
    __tablename__ = 'inventario'
    idInventario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idIngrediente = db.Column(db.Integer, db.ForeignKey('ingredientes.idIngrediente', ondelete="CASCADE"), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    ingrediente = db.relationship('Ingredientes', backref=db.backref('inventarios', cascade="all, delete-orphan"))
    detalles_venta = db.relationship('DetalleVenta', backref='inventario', cascade="all, delete-orphan")
    mermas = db.relationship('Mermas', backref='inventario', cascade="all, delete-orphan")

# Modelo Detalle Venta
class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    idDetalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idVenta = db.Column(db.Integer, db.ForeignKey('ventas.idVenta', ondelete="CASCADE"), nullable=False)
    idIngrediente = db.Column(db.Integer, db.ForeignKey('inventario.idInventario', ondelete="CASCADE"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    venta = db.relationship('Ventas', backref=db.backref('detalles_venta', cascade="all, delete-orphan"))

# Modelo Mermas
class Mermas(db.Model):
    __tablename__ = 'mermas'
    idMerma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.Enum('Producto Dañado', 'Insumo Desperdiciado', 'Insumo Caduco', 'Galletas Caducas',
                            name='tipo_merma'), nullable=False)
    idIngrediente = db.Column(db.Integer, db.ForeignKey('inventario.idInventario', ondelete="SET NULL"))
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)