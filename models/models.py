from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    rol = db.Column(db.Enum('Admin', 'Ventas', 'Cocina', 'Cliente', name='roles'), nullable=False)
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)

class Proveedores(db.Model):
    __tablename__ = 'Proveedores'
    idProveedor = db.Column(db.Integer, primary_key=True)
    nombreProveedor = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.Text)
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)

class PagoProveedores(db.Model):
    __tablename__ = 'PagoProveedores'
    idPagoProveedor = db.Column(db.Integer, primary_key=True)
    idProveedorFK = db.Column(db.Integer, db.ForeignKey('Proveedores.idProveedor'), nullable=False)
    cantidadPago = db.Column(db.Integer, nullable=False)
    ingrediente = db.Column(db.String(100), nullable=False)
    cantidadIngrediente = db.Column(db.Integer, nullable=False)
    proveedor = db.relationship('Proveedores', backref='pagos')

class MateriasPrimas(db.Model):
    __tablename__ = 'MateriasPrimas'
    idMateriaPrima = db.Column(db.Integer, primary_key=True)
    idProveedorFK = db.Column(db.Integer, db.ForeignKey('Proveedores.idProveedor'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    unidadMedida = db.Column(db.Enum('gramo', 'kilogramo', 'litro', 'mililitro', 'pieza', 'bulto', name='unidades_medida'), nullable=False)
    cantidadDisponible = db.Column(db.Numeric(10,2), default=0, nullable=False)
    cantidadMinima = db.Column(db.Numeric(10,2), default=0, nullable=False)
    precioCompra = db.Column(db.Numeric(10,2), nullable=False)
    fechaCaducidad = db.Column(db.Date)
    fechaUltimaCompra = db.Column(db.Date)
    proveedor = db.relationship('Proveedores', backref='materiasPrimas')

class Recetas(db.Model):
    __tablename__ = 'Recetas'
    idReceta = db.Column(db.Integer, primary_key=True)
    nombreReceta = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    ingredienteEspecial = db.Column(db.String(50), nullable=False)
    cantidadGalletasProducidas = db.Column(db.Integer, nullable=False)
    tiempoPreparacion = db.Column(db.Integer, nullable=False)
    diasCaducidad = db.Column(db.Integer, nullable=False)
    activa = db.Column(db.Boolean, default=True)
    ingredientes = db.relationship('IngredientesReceta', backref='receta', cascade='all, delete-orphan')
    galletas = db.relationship('Galletas', backref='receta')

class IngredientesReceta(db.Model):
    __tablename__ = 'IngredientesReceta'
    
    idIngredienteReceta = db.Column(db.Integer, primary_key=True)
    idRecetaFK = db.Column(db.Integer, db.ForeignKey('Recetas.idReceta'), nullable=False)
    idMateriaPrimaFK = db.Column(db.Integer, db.ForeignKey('MateriasPrimas.idMateriaPrima'), nullable=False)
    cantidadNecesaria = db.Column(db.Numeric(10,2), nullable=False)
    observaciones = db.Column(db.Text)
    materia_prima = db.relationship('MateriasPrimas')

class Galletas(db.Model):
    __tablename__ = 'Galletas'
    idGalleta = db.Column(db.Integer, primary_key=True)
    idRecetaFK = db.Column(db.Integer, db.ForeignKey('Recetas.idReceta'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    costoGalleta = db.Column(db.Numeric(10,2), nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    descripcion = db.Column(db.Text)
    activa = db.Column(db.Boolean, default=True)


class InventarioGalletas(db.Model):
    __tablename__ = 'InventarioGalletas'
    
    idInventarioGalleta = db.Column(db.Integer, primary_key=True)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    fechaProduccion = db.Column(db.Date, nullable=False)
    fechaCaducidad = db.Column(db.Date, nullable=False)
    lote = db.Column(db.String(50))
    disponible = db.Column(db.Boolean, default=True)
    

class Pedidos(db.Model):
    __tablename__ = 'Pedidos'
    
    idPedido = db.Column(db.Integer, primary_key=True)
    idClienteFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    fechaPedido = db.Column(db.DateTime, default=datetime.utcnow)
    fechaEntrega = db.Column(db.Date)
    total = db.Column(db.Numeric(10,2), nullable=False)
    estado = db.Column(db.Enum('Pendiente', 'En Proceso', 'Listo', 'Entregado', 'Cancelado', name='estado_pedido'), default='Pendiente')
    observaciones = db.Column(db.Text)
    
    cliente = db.relationship('Usuarios', backref='pedidos')
    detalles = db.relationship('DetallePedido', backref='pedido', cascade='all, delete-orphan')

class DetallePedido(db.Model):
    __tablename__ = 'DetallePedido'
    
    idDetallePedido = db.Column(db.Integer, primary_key=True)
    idPedidoFK = db.Column(db.Integer, db.ForeignKey('Pedidos.idPedido'), nullable=False)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precioUnitario = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(10,2), nullable=False)
    
    galleta = db.relationship('Galletas')

class Ventas(db.Model):
    __tablename__ = 'Ventas'
    
    idVenta = db.Column(db.Integer, primary_key=True)
    idUsuarioFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    fechaVenta = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Numeric(10,2), nullable=False)
    montoRecibido = db.Column(db.Numeric(10,2), nullable=False)
    cambio = db.Column(db.Numeric(10,2), nullable=False)
    
    usuario = db.relationship('Usuarios', backref='ventas')
    detalles = db.relationship('DetalleVenta', backref='venta', cascade='all, delete-orphan')

class DetalleVenta(db.Model):
    __tablename__ = 'DetalleVenta'
    
    idDetalleVenta = db.Column(db.Integer, primary_key=True)
    idVentaFK = db.Column(db.Integer, db.ForeignKey('Ventas.idVenta'), nullable=False)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precioUnitario = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(10,2), nullable=False)
    
    galleta = db.relationship('Galletas')

class Produccion(db.Model):
    __tablename__ = 'Produccion'
    
    idProduccion = db.Column(db.Integer, primary_key=True)
    idRecetaFK = db.Column(db.Integer, db.ForeignKey('Recetas.idReceta'), nullable=False)
    idUsuarioFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    fechaProduccion = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad = db.Column(db.Integer, nullable=False)
    
    receta = db.relationship('Recetas', backref='producciones')
    usuario = db.relationship('Usuarios', backref='producciones')

class SolicitudesProduccion(db.Model):
    __tablename__ = 'SolicitudesProduccion'
    
    idSolicitud = db.Column(db.Integer, primary_key=True)
    idUsuarioFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    cantidadSolicitada = db.Column(db.Integer, nullable=False)
    fechaSolicitud = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Enum('Pendiente', 'Aprobada', 'Rechazada', 'Completada', name='estado_solicitud'), default='Pendiente')
    
    usuario = db.relationship('Usuarios', backref='solicitudes')
    galleta = db.relationship('Galletas', backref='solicitudes')

class Mermas(db.Model):
    __tablename__ = 'Mermas'
    
    idMerma = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum('Materia Prima', 'Galleta Terminada', name='tipo_merma'), nullable=False)
    idMateriaPrimaFK = db.Column(db.Integer, db.ForeignKey('MateriasPrimas.idMateriaPrima'))
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'))
    cantidad = db.Column(db.Numeric(10,2), nullable=False)
    motivo = db.Column(db.Enum('Caducidad', 'Producción', 'Dañado', 'Otro', name='motivo_merma'), nullable=False)
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)
    idUsuarioFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    
    materiaPrima = db.relationship('MateriasPrimas')
    galleta = db.relationship('Galletas')
    usuario = db.relationship('Usuarios', backref='mermas')

class EstadoGalleta(db.Model):
    __tablename__ = 'EstadoGalleta'
    idEstado = db.Column(db.Integer, primary_key=True)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    estatus = db.Column(db.Enum('Pendiente', 'Aprobada', 'Completada'), nullable=False)