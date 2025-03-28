from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import Usuario
from werkzeug.security import check_password_hash
from models.formsLogin import LoginForm
from controller.auth import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/menuAdmin", methods=["GET", "POST"])
@admin_required
def menuAdmin():
    return render_template("menuAdmin.html")

