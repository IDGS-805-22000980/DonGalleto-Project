from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
from models import db
from models import Galleta
from models import Galleta
import forms



app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()


@app.route('/')
def index():
    return render_template('conocenos.html')


@app.route("/conocenos")
def conocenos():
    return render_template("conocenos.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/menuUsuario")
def menuUsuario():
    create_form = forms.GalletaForm(request.form)
    galletas = Galleta.query.all()  # Obtiene todas las galletas de la base de datos
    return render_template("menuUsuario.html", form=create_form, galletas=galletas)


@app.route("/registrarClientes", methods=["GET", "POST"])
def registrarClientes():
    return render_template("registrarClientes.html")

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)