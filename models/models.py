from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    rol = db.Column(db.Enum('Admin', 'Ventas', 'Cocina', 'Cliente'), nullable=False)
    fechaRegistro = db.Column(db.DateTime, default=db.func.current_timestamp())

class Proveedores(db.Model):
    __tablename__ = 'Proveedores'
    idProveedor = db.Column(db.Integer, primary_key=True)
    nombreProveedor = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.Text)
    fechaRegistro = db.Column(db.DateTime, default=db.func.current_timestamp())

class MateriasPrimas(db.Model):
    __tablename__ = 'MateriasPrimas'
    idMateriaPrima = db.Column(db.Integer, primary_key=True)
    idProveedorFK = db.Column(db.Integer, db.ForeignKey('Proveedores.idProveedor'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    unidadMedida = db.Column(db.Enum('gramo', 'kilogramo', 'litro', 'mililitro', 'pieza', 'bulto'), nullable=False)
    cantidadDisponible = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    cantidadMinima = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    precioCompra = db.Column(db.Numeric(10, 2), nullable=False)
    porcentajeMerma = db.Column(db.Numeric(5, 2), default=0, nullable=False)
    fechaCaducidad = db.Column(db.Date)
    fechaUltimaCompra = db.Column(db.Date)

class Recetas(db.Model):
    __tablename__ = 'Recetas'
    idReceta = db.Column(db.Integer, primary_key=True)
    nombreReceta = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    cantidadGalletasProducidas = db.Column(db.Integer, nullable=False)
    tiempoPreparacion = db.Column(db.Integer, nullable=False)
    diasCaducidad = db.Column(db.Integer, nullable=False)
    activa = db.Column(db.Boolean, default=True)

class IngredientesReceta(db.Model):
    __tablename__ = 'IngredientesReceta'
    idIngredienteReceta = db.Column(db.Integer, primary_key=True)
    idRecetaFK = db.Column(db.Integer, db.ForeignKey('Recetas.idReceta'), nullable=False)
    idMateriaPrimaFK = db.Column(db.Integer, db.ForeignKey('MateriasPrimas.idMateriaPrima'), nullable=False)
    cantidadNecesaria = db.Column(db.Numeric(10, 2), nullable=False)
    observaciones = db.Column(db.Text)

class Galletas(db.Model):
    __tablename__ = 'Galletas'
    idGalleta = db.Column(db.Integer, primary_key=True)
    idRecetaFK = db.Column(db.Integer, db.ForeignKey('Recetas.idReceta'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    activa = db.Column(db.Boolean, default=True)

class Presentaciones(db.Model):
    __tablename__ = 'Presentaciones'
    idPresentacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)

class PreciosGalletas(db.Model):
    __tablename__ = 'PreciosGalletas'
    idPrecioGalleta = db.Column(db.Integer, primary_key=True)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    idPresentacionFK = db.Column(db.Integer, db.ForeignKey('Presentaciones.idPresentacion'), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    db.UniqueConstraint(idGalletaFK, idPresentacionFK)

class InventarioGalletas(db.Model):
    __tablename__ = 'InventarioGalletas'
    idInventarioGalleta = db.Column(db.Integer, primary_key=True)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    idPresentacionFK = db.Column(db.Integer, db.ForeignKey('Presentaciones.idPresentacion'), nullable=False)
    cantidad = db.Column(db.Integer, default=0, nullable=False)
    fechaProduccion = db.Column(db.Date, nullable=False)
    fechaCaducidad = db.Column(db.Date, nullable=False)
    lote = db.Column(db.String(50))
    disponible = db.Column(db.Boolean, default=True)

class Pedidos(db.Model):
    __tablename__ = 'Pedidos'
    idPedido = db.Column(db.Integer, primary_key=True)
    idClienteFK = db.Column(db.Integer, db.ForeignKey('Usuarios.idUsuario'), nullable=False)
    fechaPedido = db.Column(db.DateTime, default=db.func.current_timestamp())
    fechaEntrega = db.Column(db.Date)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('Pendiente', 'En Proceso', 'Listo', 'Entregado', 'Cancelado'), default='Pendiente')
    observaciones = db.Column(db.Text)

class EstadoGalleta(db.Model):
    __tablename__ = 'EstadoGalleta'
    idEstado = db.Column(db.Integer, primary_key=True)
    idGalletaFK = db.Column(db.Integer, db.ForeignKey('Galletas.idGalleta'), nullable=False)
    estatus = db.Column(db.Enum('Pendiente', 'Aprobada', 'Rechazada', 'Completada'), nullable=False)

class Tickets(db.Model):
    __tablename__ = 'Tickets'
    idTicket = db.Column(db.Integer, primary_key=True)
    idVentaFK = db.Column(db.Integer, db.ForeignKey('Ventas.idVenta'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fechaGeneracion = db.Column(db.DateTime, default=db.func.current_timestamp())
    codigoQR = db.Column(db.String(255))
