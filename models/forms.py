from datetime import datetime, timedelta
from wtforms import DateField, DateTimeField, DecimalField, Form, HiddenField, SelectField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange

class GalletaForm(FlaskForm):
    nombre_receta = StringField('Nombre', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired()])
    cantidad_galleta_producida = IntegerField('Cantidad de Galletas producidas', validators=[DataRequired()])
    dias_caducidad = IntegerField('Dias de caducidad', validators=[DataRequired()])
    inventario = IntegerField('Inventario', validators=[DataRequired()])
    
class ProductoForm(FlaskForm):
    idProduccion = IntegerField('Id de produccion', validators=[DataRequired()])
    idReceta = IntegerField('Id de receta', validators=[DataRequired()])
    fechaCaducidad = DateField('Fecha de caducidad', validators=[DataRequired()])
    fechaProduccion = DateField('Fecha de produccion', validators=[DataRequired()])
    receta = SelectField('Receta', choices=[(1, 'Receta 1'), (2, 'Receta 2'), (3, 'Receta 3'), (4, 'Receta 4'), (5, 'Receta 5')])

class PedidoForm(FlaskForm):
    idUsuario = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    direccionEntrega = StringField('Dirección de Entrega', validators=[DataRequired()])
    telefonoContacto = StringField('Teléfono de Contacto', validators=[DataRequired()])
    notas = TextAreaField('Notas Adicionales')
    metodo_pago = SelectField('Método de Pago', 
                            choices=[('Efectivo', 'Efectivo'), 
                                    ('Tarjeta', 'Tarjeta'), 
                                    ('Transferencia', 'Transferencia')],
                            validators=[DataRequired()])
    submit = SubmitField('Crear Pedido')

class DetallePedidoForm(FlaskForm):
    idPedido = HiddenField()
    idGalleta = SelectField('Galleta', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    precioUnitario = DecimalField('Precio Unitario', validators=[DataRequired()])
    personalizacion = TextAreaField('Personalización')
    submit = SubmitField('Agregar al Pedido')

class ProcesarPedidoForm(FlaskForm):
    idPedido = HiddenField()
    submit = SubmitField('Iniciar Producción')
    cancelar = SubmitField('Cancelar Pedido')


class ProduccionForm(FlaskForm):
    idReceta = SelectField(
        'Receta', 
        coerce=int, 
        validators=[DataRequired()],
        choices=[]  # Se llenará dinámicamente
    )
    cantidad = IntegerField(
        'Cantidad a Producir', 
        validators=[
            DataRequired(),
            NumberRange(min=1, message="La cantidad debe ser al menos 1")
        ]
    )
    submit = SubmitField('Iniciar Producción')
    submit = SubmitField('Iniciar Producción')
    
class IngredienteRecetaForm(FlaskForm):
    idReceta = HiddenField()
    idIngrediente = SelectField('Ingrediente', coerce=int, validators=[DataRequired()])
    cantidad = DecimalField('Cantidad', validators=[DataRequired(), NumberRange(min=0.01)])
    unidadMedida = SelectField('Unidad de Medida', 
                            choices=[('gramo', 'Gramos'), 
                                    ('kilogramo', 'Kilogramos'), 
                                    ('litro', 'Litros'), 
                                    ('mililitro', 'Mililitros'), 
                                    ('pieza', 'Piezas'), 
                                    ('bulto', 'Bultos')],
                            validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones')
    submit = SubmitField('Agregar Ingrediente')


class InventarioForm(FlaskForm):
    idIngrediente = SelectField(
        'Ingrediente', 
        coerce=int, 
        validators=[DataRequired()],
        choices=[]  
    )
    cantidad = DecimalField(
        'Cantidad', 
        validators=[DataRequired(), NumberRange(min=0)],
        places=2
    )
    submit = SubmitField('Actualizar Inventario')
class CambioEstadoForm(FlaskForm):
    idPedido = HiddenField()
    nuevoEstado = SelectField('Nuevo Estado', 
                            choices=[('Pendiente', 'Pendiente'), 
                                    ('En proceso', 'En proceso'), 
                                    ('Listo para recoger', 'Listo para recoger'), 
                                    ('Entregado', 'Entregado'), 
                                    ('Cancelado', 'Cancelado')],
                            validators=[DataRequired()])
    comentarios = TextAreaField('Comentarios')
    submit = SubmitField('Cambiar Estado')