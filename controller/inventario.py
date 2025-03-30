from flask import render_template, Blueprint
from models.models import InventarioGalletas, Galletas, db

inventarioTerminado = Blueprint('inventarioTerminado', __name__)

@inventarioTerminado.route('/inventario')
def inventario():
    inventario = (
        db.session.query(Galletas.nombre, InventarioGalletas.cantidad)
        .join(InventarioGalletas, Galletas.idGalleta == InventarioGalletas.idGalletaFK)
        .all()
    )
    return render_template('inventario.html', inventario=inventario)
