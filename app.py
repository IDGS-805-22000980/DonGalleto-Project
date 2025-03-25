from flask import Flask, render_template, request, redirect, url_for, blueprints
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from models.config import DevelopmentConfig
from models.models import db
from models.models import Galleta
from models.forms import GalletaForm
import models.forms
from controller.menuUsuario import menuGalleta


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

app.register_blueprint(menuGalleta)

@app.route('/')
def index():
    return render_template('conocenos.html')


@app.route("/conocenos")
def conocenos():
    return render_template("conocenos.html")

@app.route("/login")
def login():
    return render_template("login.html")



@app.route("/registrarClientes", methods=["GET", "POST"])
def registrarClientes():
    return render_template("registrarClientes.html")

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)