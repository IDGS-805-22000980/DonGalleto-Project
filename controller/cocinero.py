from flask import Flask, render_template, request, Blueprint, flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from models.models import db, Receta, InventarioGalletas, Produccion, Ingredientes, IngredienteReceta, Inventario, Pedido,DetallePedido, SeguimientoPedidos
from models.forms import ProduccionForm, PedidoForm, CambioEstadoForm
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload

chefCocinero = Blueprint('chefCocinero', __name__)


@chefCocinero.route('/produccion')
def produccion():
    pedidos = Pedido.query.all()
    form = CambioEstadoForm()
    for pedido in pedidos:
        print(f"Pedido ID en Flask: {pedido.idPedido}")  # DEBUG
    return render_template('produccion.html', pedidos=pedidos, form=form)


@chefCocinero.route('/cambiar_estado', methods=['POST'])
def cambiar_estado():
    
    id_pedido = request.form.getlist("idPedido")
    nuevo_estado = request.form.get("nuevoEstado")

    print(f"ID Pedido recibido: {id_pedido}")  # Para ver cómo llega el valor
    print(f"Nuevo estado recibido: {nuevo_estado}")

    # Filtra valores vacíos
    id_pedido = [x for x in id_pedido if x]  # Elimina valores vacíos

    if not id_pedido:
        flash("Pedido no encontrado", "danger")
        return redirect(url_for('chefCocinero.produccion'))

    id_pedido = id_pedido[0]  # Tomamos solo el primer valor
    pedido = Pedido.query.get(id_pedido)

    if not pedido:
        flash("Pedido no encontrado en la base de datos", "danger")
        return redirect(url_for('chefCocinero.produccion'))

    pedido.estado = nuevo_estado
    db.session.commit()

    print(f"Estado actualizado en la base de datos: {pedido.estado}")

    flash("Estado actualizado correctamente", "success")
    return redirect(url_for('chefCocinero.produccion'))
