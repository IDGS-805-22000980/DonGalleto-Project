from flask import render_template, Blueprint
from models.models import InventarioGalletas, Galletas, db

# Blueprint
inventarioTerminado = Blueprint('inventarioTerminado', __name__)

@inventarioTerminado.route('/inventario')
def inventario():
    inventario_data = (
        db.session.query(Galletas.nombre, InventarioGalletas.stock, Galletas.descripcion)
        .join(InventarioGalletas, Galletas.idGalleta == InventarioGalletas.idGalletaFK)
        .all()
    )
    return render_template('inventario.html', inventario=inventario_data)