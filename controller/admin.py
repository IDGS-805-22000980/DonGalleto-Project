from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import db, Usuarios, Galletas, Presentaciones, PreciosGalletas, Pedidos, DetallePedido, Ventas, DetalleVenta
from werkzeug.security import check_password_hash, generate_password_hash
from models.formsAdmin import RegistrarEmpleadosForm
from controller.auth import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/menuAdmin", methods=['GET', 'POST'])
@admin_required
def menuAdmin():
    return render_template("admin/menuAdmin.html")

@admin_bp.route("/AgregarEmpleado", methods=["GET", "POST"])
@admin_required
def agregarEmpleado():
    form = RegistrarEmpleadosForm()

    if form.validate_on_submit():
        try:
            # Verificar si el email ya existe
            if Usuario.query.filter_by(email=form.email.data).first():
                flash('Este email ya está registrado', 'error')
                return redirect(url_for('admin.AgregarEmpleado'))
            
            # Crear nuevo usuario
            nuevo_empleado = Usuario(
                nombre=form.nombre.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                rol=form.rol.data
            )
            
            db.session.add(nuevo_empleado)
            db.session.commit()
            
            flash('Empleado registrado exitosamente!', 'success')
            return redirect(url_for('admin.menuAdmin'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'error')
    
    return render_template('admin/AgregarEmpleado.html', form=form)


