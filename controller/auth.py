from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import db, Usuario
from werkzeug.security import check_password_hash, generate_password_hash
from models.formsLogin import LoginForm, RegistrarClientesForm
from functools import wraps

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Buscar usuario en la BD
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.password, password):
            session['user_id'] = usuario.idUsuario
            session['user_rol'] = usuario.rol
            
            # Redirección según rol
            if usuario.rol == 'Admin':
                return redirect(url_for('admin.menuAdmin'))
            elif usuario.rol == 'Ventas':
                return redirect(url_for('ventas.menuVentas'))
            elif usuario.rol == 'Cocina':
                return redirect(url_for('cocina.menuCocina'))
            elif usuario.rol == 'Cliente':
                return redirect(url_for('cliente.menuCliente'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html', form=form)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('conocenos'))

@auth_bp.route("/registrarClientes", methods=['GET', 'POST'])
def registrarClientes():
    form = RegistrarClientesForm()
    
    # Establecer Cliente como valor por defecto
    form.rol.data = 'Cliente'  # Opcional: puedes quitarlo si quieres que seleccionen
    
    if form.validate_on_submit():
        try:
            # Verificar si el email ya existe
            if Usuario.query.filter_by(email=form.email.data).first():
                flash('Este email ya está registrado', 'error')
                return redirect(url_for('auth.registrarClientes'))
            
            # Crear nuevo usuario
            nuevo_usuario = Usuario(
                nombre=form.nombre.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                rol=form.rol.data
            )
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            flash('Registro exitoso! Por favor inicia sesión', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'error')
    
    return render_template('registrarClientes.html', form=form)


# Decorador para Admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_rol' not in session or session['user_rol'] != 'Admin':
            flash("Acceso restringido: Solo para administradores", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para Ventas
def ventas_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_rol' not in session or session['user_rol'] != 'Ventas':
            flash("Acceso restringido: Solo para personal de ventas", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para Cocina
def cocina_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_rol' not in session or session['user_rol'] != 'Cocina':
            flash("Acceso restringido: Solo para personal de cocina", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para Cliente
def cliente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_rol' not in session or session['user_rol'] != 'Cliente':
            flash("Acceso restringido: Solo para clientes", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
