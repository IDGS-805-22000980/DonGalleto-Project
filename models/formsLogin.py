from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators
from wtforms import StringField, PasswordField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

class RegistrarClientesForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    rol = SelectField('Rol', choices=[
        ('Cliente', 'Cliente'),
        ('Admin', 'Admin'),
        ('Ventas', 'Ventas'),
        ('Cocina', 'Cocina')
    ], validators=[DataRequired()])