from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import db, Pedido, SeguimientoPedido, Usuario
from datetime import datetime
from controller.auth import ventas_required

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route("/menuVentas")
@ventas_required
def menuVentas():
    return render_template("menuVentas.html")

@ventas_bp.route("/pedidos")
@ventas_required
def listar_pedidos():
    # Obtener todos los pedidos ordenados por fecha descendente
    estado_filtro = request.args.get('estado', 'all')
    
    query = Pedido.query.order_by(Pedido.fechaPedido.desc())
    
    if estado_filtro != 'all':
        query = query.filter_by(estado=estado_filtro)
    
    pedidos = query.all()
    
    return render_template("pedidos_ventas.html", 
                        pedidos=pedidos,
                        estado_actual=estado_filtro)

@ventas_bp.route("/pedido/<int:id>")
@ventas_required
def detalle_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    historial = SeguimientoPedido.query.filter_by(idPedido=id).order_by(SeguimientoPedido.fechaCambio.desc()).all()
    return render_template("detalle_pedido_ventas.html", 
                         pedido=pedido,
                         historial=historial)

@ventas_bp.route("/actualizar_estado/<int:id>", methods=["POST"])
@ventas_required
def actualizar_estado(id):
    pedido = Pedido.query.get_or_404(id)
    nuevo_estado = request.form.get('estado')
    comentarios = request.form.get('comentarios', '').strip()
    
    if not nuevo_estado or nuevo_estado not in ['Pendiente', 'En proceso', 'Listo para recoger', 'Entregado', 'Cancelado']:
        flash('Estado no válido', 'danger')
        return redirect(url_for('ventas.detalle_pedido', id=id))
    
    try:
        # Registrar el cambio de estado
        seguimiento = SeguimientoPedido(
            idPedido=pedido.idPedido,
            estadoAnterior=pedido.estado,
            estadoNuevo=nuevo_estado,
            idUsuarioCambio=session['user_id'],
            comentarios=comentarios
        )
        
        # Actualizar el estado del pedido
        pedido.estado = nuevo_estado
        
        # Si el pedido se marca como Entregado o Cancelado, registrar hora
        if nuevo_estado in ['Entregado', 'Cancelado']:
            pedido.fechaFinalizacion = datetime.utcnow()
        
        db.session.add(seguimiento)
        db.session.commit()
        
        flash(f'Estado actualizado a {nuevo_estado}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar estado: {str(e)}', 'danger')
    
    return redirect(url_for('ventas.detalle_pedido', id=id))