from flask import Flask, render_template, request, redirect, url_for, blueprints
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from models.config import DevelopmentConfig
from models.models import db, Usuarios, Galletas, Presentaciones, PreciosGalletas, Pedidos, DetallePedido, Ventas, DetalleVenta
from models.forms import GalletaForm
from werkzeug.security import generate_password_hash
import models.forms
from controller.auth import auth_bp
from controller.admin import admin_bp
from controller.ventas import ventas_bp
from controller.cocina import cocina_bp
from controller.cliente import cliente_bp


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Inicializar extenciones
csrf=CSRFProtect()
csrf.init_app(app)
db.init_app(app)


# Registrar Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(cocina_bp)
app.register_blueprint(cliente_bp)

@app.route('/')
def index():
    return render_template('conocenos.html')


@app.route("/conocenos")
def conocenos():
    return render_template("conocenos.html")




if __name__ == "__main__":
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        # Verificar y crear usuario de prueba
        try:
            if not Usuarios.query.filter_by(email="admin@example.com").first():
                usuario_prueba = Usuarios(
                    nombre="Admin",
                    email="admin@example.com",
                    password=generate_password_hash("admin1234"),
                    rol="Admin"
                )
                db.session.add(usuario_prueba)
                db.session.commit()
                print("✅ Usuario de prueba creado")
        except Exception as e:
            print(f"Error al crear usuario de prueba: {str(e)}")
            db.session.rollback()
    
    app.run(debug=True, port=5000)