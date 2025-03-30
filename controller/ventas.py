from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import db, Pedidos, DetallePedido, Galletas, InventarioGalletas
from datetime import datetime
from controller.auth import ventas_required

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route("/menuVentas", methods=["GET", "POST"])
@ventas_required
def menuVentas():
    # Obtener todos los pedidos ordenados por fecha
    pedidos = Pedidos.query.order_by(Pedidos.fechaPedido.desc()).all()
    return render_template("ventas/menuVentas.html", pedidos=pedidos)

@ventas_bp.route("/cambiar_estado/<int:pedido_id>", methods=["POST"])
@ventas_required
def cambiar_estado(pedido_id):
    pedido = Pedidos.query.get_or_404(pedido_id)
    nuevo_estado = request.form.get('nuevo_estado')
    
    if not nuevo_estado:
        flash('No se especificó un estado nuevo', 'error')
        return redirect(url_for('ventas.menuVentas'))
    
    try:
        estado_anterior = pedido.estado
        pedido.estado = nuevo_estado
        
        # Si cambiamos a "Entregado", actualizar inventario
        if nuevo_estado == 'Entregado' and estado_anterior != 'Entregado':
            actualizar_inventario(pedido)
            
        db.session.commit()
        flash(f'Estado del pedido #{pedido_id} cambiado a {nuevo_estado}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado: {str(e)}', 'error')
    
    return redirect(url_for('ventas.menuVentas'))

def actualizar_inventario(pedido):
    """Actualiza el inventario cuando un pedido es marcado como entregado"""
    for detalle in pedido.detalles:
        # Buscar el inventario de la galleta en la presentación correspondiente
        inventario = InventarioGalletas.query.filter_by(
            idGalletaFK=detalle.idGalletaFK,
            idPresentacionFK=detalle.idPresentacionFK
        ).first()
        
        if inventario:
            if inventario.cantidad >= detalle.cantidad:
                inventario.cantidad -= detalle.cantidad
            else:
                raise ValueError(f'No hay suficiente inventario para {detalle.galleta.nombre} - {detalle.presentacion.nombre}')
        else:
            raise ValueError(f'No se encontró inventario para {detalle.galleta.nombre} - {detalle.presentacion.nombre}')


@ventas_bp.route("/detalle_pedido/<int:pedido_id>")
@ventas_required
def detalle_pedido(pedido_id):
    pedido = Pedidos.query.get_or_404(pedido_id)
    return render_template("ventas/detalle_pedido.html", pedido=pedido)