from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import datetime

db = SQLAlchemy()

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    rol = db.Column(db.Enum('Admin', 'Ventas', 'Cocina', 'Cliente'), nullable=False)
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)

class Proveedores(db.Model):
    __tablename__ = 'Proveedores'
    idProveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreProveedor = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.Text)
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)

class MateriasPrimas(db.Model):
    __tablename__ = 'MateriasPrimas'
    idMateriaPrima = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProveedorFK = db.Column(db.Integer, db.ForeignKey('Proveedores.idProveedor'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    unidadMedida = db.Column(db.Enum('gramo', 'kilogramo', 'litro', 'mililitro', 'pieza', 'bulto'), nullable=False)
    cantidadDisponible = db.Column(Numeric(10, 2), default=0, nullable=False)
    cantidadMinima = db.Column(Numeric(10, 2), default=0, nullable=False)
    precioCompra = db.Column(Numeric(10, 2), nullable=False)
    porcentajeMerma = db.Column(Numeric(5, 2), default=0, nullable=False)
    fechaCaducidad = db.Column(db.Date)
    fechaUltimaCompra = db.Column(db.Date)
    
    proveedor = db.relationship('Proveedores', backref='materias_primas')

class Recetas(db.Model):
    __tablename__ = 'Recetas'
    idReceta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreReceta = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    cantidadGalletasProducidas = db.Column(db.Integer, nullable=False)
    tiempoPreparacion = db.Column(db.Integer, nullable=False)
    diasCaducidad = db.Column(db.Integer, nullable=False)
    activa = db.Column(db.Boolean, default=True)

class IngredientesReceta(db.Model):
    __tablename__ = 'IngredientesReceta'
    idIngredienteReceta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idRecetaFK = db.Column(db.Integer, db.ForeignKey('Recetas.idReceta'), nullable=False)
    idMateriaPrimaFK = db.Column(db.Integer, db.ForeignKey('MateriasPrimas.idMateriaPrima'), nullable=False)
    cantidadNecesaria = db.Column(Numeric(10, 2), nullable=False)
    observaciones = db.Column(db.Text)
    
    receta = db.relationship('Recetas', backref='ingredientes')
    materia_prima = db.relationship('MateriasPrimas', backref='recetas')

class Galletas(db.Model):
    __tablename__ = 'Galletas'
    idGalleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idRecetaFK = db.Column(db.Integer, db.ForeignKey('Recetas.idReceta'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    activa = db.Column(db.Boolean, default=True)
    
    receta = db.relationship('Recetas', backref='galletas')

class Presentaciones(db.Model):
    __tablename__ = 'Presentaciones'
    idPresentacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)

class PreciosGalletas(db.Model):
    __tablename__ = 'PreciosGalletas'
    idPrecioGalleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    idPresentacionFK = db.Column(db.Integer, db.ForeignKey('Presentaciones.idPresentacion'), nullable=False)
    precio = db.Column(Numeric(10, 2), nullable=False)
    
    galleta = db.relationship('Galletas', backref='precios')
    presentacion = db.relationship('Presentaciones', backref='precios')
    
    __table_args__ = (
        db.UniqueConstraint('idGalletaFK', 'idPresentacionFK'),
    )

class InventarioGalletas(db.Model):
    __tablename__ = 'InventarioGalletas'
    idInventarioGalleta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    idPresentacionFK = db.Column(db.Integer, db.ForeignKey('Presentaciones.idPresentacion'), nullable=False)
    cantidad = db.Column(db.Integer, default=0, nullable=False)
    fechaProduccion = db.Column(db.Date, nullable=False)
    fechaCaducidad = db.Column(db.Date, nullable=False)
    lote = db.Column(db.String(50))
    disponible = db.Column(db.Boolean, default=True)
    
    galleta = db.relationship('Galletas', backref='inventario')
    presentacion = db.relationship('Presentaciones', backref='inventario')

class Pedidos(db.Model):
    __tablename__ = 'Pedidos'
    idPedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idClienteFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    fechaPedido = db.Column(db.DateTime, default=datetime.utcnow)
    fechaEntrega = db.Column(db.Date)
    total = db.Column(Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('Pendiente', 'En Proceso', 'Listo', 'Entregado', 'Cancelado'), default='Pendiente')
    observaciones = db.Column(db.Text)
    
    cliente = db.relationship('Usuarios', backref='pedidos')

class DetallePedido(db.Model):
    __tablename__ = 'DetallePedido'
    idDetallePedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idPedidoFK = db.Column(db.Integer, db.ForeignKey('Pedidos.idPedido'), nullable=False)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    idPresentacionFK = db.Column(db.Integer, db.ForeignKey('Presentaciones.idPresentacion'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precioUnitario = db.Column(Numeric(10, 2), nullable=False)
    subtotal = db.Column(Numeric(10, 2), nullable=False)
    
    pedido = db.relationship('Pedidos', backref='detalles')
    galleta = db.relationship('Galletas', backref='detalles_pedido')
    presentacion = db.relationship('Presentaciones', backref='detalles_pedido')

class Ventas(db.Model):
    __tablename__ = 'Ventas'
    idVenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuarioFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    fechaVenta = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(Numeric(10, 2), nullable=False)
    pago = db.Column(Numeric(10, 2), nullable=False)
    cambio = db.Column(Numeric(10, 2), nullable=False)
    metodoPago = db.Column(db.Enum('Efectivo'), nullable=False)
    
    usuario = db.relationship('Usuarios', backref='ventas')

class DetalleVenta(db.Model):
    __tablename__ = 'DetalleVenta'
    idDetalleVenta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idVentaFK = db.Column(db.Integer, db.ForeignKey('Ventas.idVenta'), nullable=False)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    idPresentacionFK = db.Column(db.Integer, db.ForeignKey('Presentaciones.idPresentacion'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precioUnitario = db.Column(Numeric(10, 2), nullable=False)
    subtotal = db.Column(Numeric(10, 2), nullable=False)
    
    venta = db.relationship('Ventas', backref='detalles')
    galleta = db.relationship('Galletas', backref='detalles_venta')
    presentacion = db.relationship('Presentaciones', backref='detalles_venta')

class Produccion(db.Model):
    __tablename__ = 'Produccion'
    idProduccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idRecetaFK = db.Column(db.Integer, db.ForeignKey('Recetas.idReceta'), nullable=False)
    idUsuarioFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    fechaProduccion = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad = db.Column(db.Integer, nullable=False)
    totalGalletas = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.Text)
    
    receta = db.relationship('Recetas', backref='producciones')
    usuario = db.relationship('Usuarios', backref='producciones')

class SolicitudesProduccion(db.Model):
    __tablename__ = 'SolicitudesProduccion'
    idSolicitud = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuarioFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    cantidadSolicitada = db.Column(db.Integer, nullable=False)
    fechaSolicitud = db.Column(db.DateTime, default=datetime.utcnow)
    fechaRequerida = db.Column(db.Date)
    estado = db.Column(db.Enum('Pendiente', 'Aprobada', 'Rechazada', 'Completada'), default='Pendiente')
    prioridad = db.Column(db.Enum('Baja', 'Media', 'Alta'), default='Media')
    
    usuario = db.relationship('Usuarios', backref='solicitudes')
    galleta = db.relationship('Galletas', backref='solicitudes')

class Mermas(db.Model):
    __tablename__ = 'Mermas'
    idMerma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.Enum('Materia Prima', 'Galleta Terminada'), nullable=False)
    idMateriaPrimaFK = db.Column(db.Integer, db.ForeignKey('MateriasPrimas.idMateriaPrima'))
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'))
    idPresentacionFK = db.Column(db.Integer, db.ForeignKey('Presentaciones.idPresentacion'))
    cantidad = db.Column(Numeric(10, 2), nullable=False)
    motivo = db.Column(db.Enum('Caducidad', 'Producción', 'Dañado', 'Otro'), nullable=False)
    fechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)
    idUsuarioFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    observaciones = db.Column(db.Text)
    
    materia_prima = db.relationship('MateriasPrimas', backref='mermas')
    galleta = db.relationship('Galletas', backref='mermas')
    presentacion = db.relationship('Presentaciones', backref='mermas')
    usuario = db.relationship('Usuarios', backref='mermas')

class Tickets(db.Model):
    __tablename__ = 'Tickets'
    idTicket = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idVentaFK = db.Column(db.Integer, db.ForeignKey('Ventas.idVenta'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fechaGeneracion = db.Column(db.DateTime, default=datetime.utcnow)
    codigoQR = db.Column(db.String(255))
    
    venta = db.relationship('Ventas', backref='tickets')