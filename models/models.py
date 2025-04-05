from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    rol = db.Column(db.Enum('Admin', 'Ventas', 'Cocina', 'Cliente', name='roles'), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_proveedor = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

class PagoProveedor(db.Model):
    __tablename__ = 'pago_proveedores'
    
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    cantidad_pago = db.Column(db.Integer, nullable=False)
    ingrediente = db.Column(db.String(100), nullable=False)
    cantidad_ingrediente = db.Column(db.Integer, nullable=False)
    
    proveedor = db.relationship('Proveedor', backref='pagos')

class MateriaPrima(db.Model):
    __tablename__ = 'materias_primas'
    
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    unidad_medida = db.Column(db.Enum('gramo', 'kilogramo', 'litro', 'mililitro', 'pieza', 'bulto', name='unidades_medida'), nullable=False)
    cantidad_disponible = db.Column(db.Numeric(10,2), default=0, nullable=False)
    cantidad_minima = db.Column(db.Numeric(10,2), default=0, nullable=False)
    precio_compra = db.Column(db.Numeric(10,2), nullable=False)
    fecha_caducidad = db.Column(db.Date)
    fecha_ultima_compra = db.Column(db.Date)
    
    proveedor = db.relationship('Proveedor', backref='materias_primas')

class Receta(db.Model):
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_receta = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    ingrediente_especial = db.Column(db.String(50), nullable=False)
    cantidad_galletas_producidas = db.Column(db.Integer, nullable=False)
    tiempo_preparacion = db.Column(db.Integer, nullable=False)
    dias_caducidad = db.Column(db.Integer, nullable=False)
    activa = db.Column(db.Boolean, default=True)
    
    ingredientes = db.relationship('IngredienteReceta', backref='receta', cascade='all, delete-orphan')
    galletas = db.relationship('Galleta', backref='receta')

class IngredienteReceta(db.Model):
    __tablename__ = 'ingredientes_receta'
    
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'), nullable=False)
    cantidad_necesaria = db.Column(db.Numeric(10,2), nullable=False)
    observaciones = db.Column(db.Text)
    
    materia_prima = db.relationship('MateriaPrima')

class Galleta(db.Model):
    __tablename__ = 'galletas'
    
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    costo_galleta = db.Column(db.Numeric(10,2), nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    descripcion = db.Column(db.Text)
    activa = db.Column(db.Boolean, default=True)
    
    inventario = db.relationship('InventarioGalleta', backref='galleta')
    detalles_pedido = db.relationship('DetallePedido', backref='galleta')
    detalles_venta = db.relationship('DetalleVenta', backref='galleta')
    solicitudes = db.relationship('SolicitudProduccion', backref='galleta')

class InventarioGalleta(db.Model):
    __tablename__ = 'inventario_galletas'
    
    id = db.Column(db.Integer, primary_key=True)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galletas.id'), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    fecha_produccion = db.Column(db.Date, nullable=False)
    fecha_caducidad = db.Column(db.Date, nullable=False)
    lote = db.Column(db.String(50))
    disponible = db.Column(db.Boolean, default=True)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_entrega = db.Column(db.Date)
    total = db.Column(db.Numeric(10,2), nullable=False)
    estado = db.Column(db.Enum('Pendiente', 'En Proceso', 'Listo', 'Entregado', 'Cancelado', name='estados_pedido'), default='Pendiente')
    observaciones = db.Column(db.Text)
    
    cliente = db.relationship('Usuario')
    detalles = db.relationship('DetallePedido', backref='pedido', cascade='all, delete-orphan')

class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galletas.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(10,2), nullable=False)

class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Numeric(10,2), nullable=False)
    costo_total = db.Column(db.Numeric(10,2), nullable=False)  # Nuevo campo
    ganancia = db.Column(db.Numeric(10,2), nullable=False) # Nuevo campo
    monto_recibido = db.Column(db.Numeric(10,2), nullable=False)
    cambio = db.Column(db.Numeric(10,2), nullable=False)
    
    usuario = db.relationship('Usuario')
    detalles = db.relationship('DetalleVenta', backref='venta', cascade='all, delete-orphan')

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galletas.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    galletas_descontadas = db.Column(db.Integer, nullable=False) #Nuevo campo
    precio_unitario = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(10,2), nullable=False)

class Produccion(db.Model):
    __tablename__ = 'produccion'
    
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_produccion = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad = db.Column(db.Integer, nullable=False)
    
    receta = db.relationship('Receta')
    usuario = db.relationship('Usuario')

class SolicitudProduccion(db.Model):
    __tablename__ = 'solicitudes_produccion'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    galleta_id = db.Column(db.Integer, db.ForeignKey('galletas.id'), nullable=False)
    cantidad_solicitada = db.Column(db.Integer, nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Enum('Pendiente', 'Aprobada', 'Rechazada', 'Completada', name='estados_solicitud'), default='Pendiente')
    
    usuario = db.relationship('Usuario')

class Merma(db.Model):
    __tablename__ = 'mermas'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum('Materia Prima', 'Galleta Terminada', name='tipos_merma'), nullable=False)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    galleta_id = db.Column(db.Integer, db.ForeignKey('galletas.id'))
    cantidad = db.Column(db.Numeric(10,2), nullable=False)
    motivo = db.Column(db.Enum('Caducidad', 'Producción', 'Dañado', 'Otro', name='motivos_merma'), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    materia_prima = db.relationship('MateriaPrima')
    galleta = db.relationship('Galleta')
    usuario = db.relationship('Usuario')