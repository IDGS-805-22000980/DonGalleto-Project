from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators
from wtforms.validators import DataRequired

class GalletaForm(FlaskForm):
    nombre_receta = StringField('Nombre', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired()])
    cantidad_galleta_producida = IntegerField('Cantidad de Galletas producidas', validators=[DataRequired()])
    dias_caducidad = IntegerField('Dias de caducidad', validators=[DataRequired()])
    inventario = IntegerField('Inventario', validators=[DataRequired()])
    