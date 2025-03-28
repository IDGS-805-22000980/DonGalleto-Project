from flask import Flask, render_template, request, Blueprint, flash
from flask_wtf.csrf import CSRFProtect
from models.models import db, Receta, InventarioGalletas
from models.forms import GalletaForm

menuGalleta = Blueprint('menuGalleta', __name__)
csrf = CSRFProtect()

@menuGalleta.route("/menuUsuario", methods=['GET'])
def menuUsuario():
    try:
        form = GalletaForm()
        galletas = Receta.query.all()
        return render_template("menuUsuario.html", form=form, galletas=galletas)
    except Exception as e:
        flash("Error al cargar las galletas: " + str(e), "danger")
        return render_template("menuUsuario.html", form=form, galletas=[])
