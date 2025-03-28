#Controller Inventario
from flask import render_template, Blueprint
from models.models import InventarioGalletas, Receta

inventarioTerminado = Blueprint('inventarioTerminado', __name__)

@inventarioTerminado.route('/inventario')
def inventario():
    inventario = InventarioGalletas.query.join(Receta).all()
    return render_template('inventario.html', inventario=inventario)
