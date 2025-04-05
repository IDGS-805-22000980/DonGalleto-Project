from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SelectField
from wtforms import EmailField
from wtforms import validators
from wtforms.validators import DataRequired
from models.models import db, Usuarios, Galletas, Pedidos, DetallePedido, Ventas, DetalleVenta




class VentaForm(FlaskForm):
    idVenta = IntegerField('Id de venta', validators=[DataRequired()])
    galleta = SelectField("Galleta", coerce=int, validators=[DataRequired()])
    presentacion = SelectField("Presentación", coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    precio = IntegerField('Precio', validators=[DataRequired()])
    fecha = StringField('Fecha', validators=[DataRequired()])
    montoRecibido = IntegerField('Monto recibido', validators=[DataRequired()])
    cambio = IntegerField('Cambio', validators=[DataRequired()])
    total = IntegerField('Total', validators=[DataRequired()])
    totalVenta = IntegerField('Total Venta', validators=[DataRequired()])
