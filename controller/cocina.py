from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import db, Usuarios, Galletas, Presentaciones, PreciosGalletas, Pedidos, DetallePedido, Ventas, DetalleVenta
from werkzeug.security import check_password_hash
from models.formsLogin import LoginForm
from controller.auth import cocina_required

cocina_bp = Blueprint('cocina', __name__)

@cocina_bp.route("/menuCocina", methods=["GET", "POST"])
@cocina_required
def menuCocina():
    return render_template("menuCocina.html")