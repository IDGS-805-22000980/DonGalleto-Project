from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators
from wtforms.validators import DataRequired

class GalletaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    precio_por_pieza = IntegerField('Precio por pieza', validators=[DataRequired()])
    precio_por_gramo = IntegerField('Precio por gramo', validators=[DataRequired()])
    cantidadGalletas = IntegerField('Cantidad de galletas', validators=[DataRequired()])