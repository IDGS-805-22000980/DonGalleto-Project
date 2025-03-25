from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from models.config import DevelopmentConfig
from models.models import db
from models.models import Galleta
from models.forms import GalletaForm
import models.forms


menuGalleta = Blueprint('menuGalleta', __name__)
csrf=CSRFProtect()

@menuGalleta.route("/menuUsuario")
def menuUsuario():
    create_form = models.forms.GalletaForm(request.form)
    galletas = Galleta.query.all()
    return render_template("menuUsuario.html", form=create_form, galletas=galletas)
