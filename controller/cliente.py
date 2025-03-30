from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import db, Galletas, Presentaciones, PreciosGalletas, Pedidos, DetallePedido
from datetime import datetime, timedelta
from models.forms import PedidoForm
from controller.auth import cliente_required

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route("/menuCliente", methods=["GET", "POST"])
@cliente_required
def menuCliente():
    # Configurar fechas mínima y máxima para entrega
    hoy = datetime.now().date()
    min_date = hoy + timedelta(days=2)  # Mínimo 2 días después
    max_date = hoy + timedelta(days=30)  # Máximo 30 días después
    
    # Preparar fechas para mostrar en formato dd/mm/yyyy
    min_date_display = min_date.strftime('%d/%m/%Y')
    max_date_display = max_date.strftime('%d/%m/%Y')
    
    # Obtener todas las galletas activas con sus precios y presentaciones
    galletas_info = []
    galletas_activas = Galletas.query.filter_by(activa=True).all()
    
    for galleta in galletas_activas:
        precios = PreciosGalletas.query.filter_by(idGalletaFK=galleta.idGalleta).all()
        for precio in precios:
            presentacion = Presentaciones.query.get(precio.idPresentacionFK)
            if presentacion:
                galletas_info.append((galleta, presentacion, precio))
    
    if request.method == 'POST':
        try:
            # Obtener y validar fecha de entrega
            fecha_entrega_str = request.form.get('fecha_entrega')
            fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%d').date()
            
            # Validaciones de fecha
            if fecha_entrega < min_date or fecha_entrega > max_date:
                flash(f'La fecha de entrega debe ser entre {min_date_display} y {max_date_display}', 'error')
                return render_template("cliente/menuCliente.html", 
                                    galletas=galletas_info,
                                    min_date=min_date.strftime('%Y-%m-%d'),
                                    max_date=max_date.strftime('%Y-%m-%d'),
                                    min_date_display=min_date_display,
                                    max_date_display=max_date_display)
            
            # Validar que no sea fin de semana (sábado=5, domingo=6)
            if fecha_entrega.weekday() >= 5:
                flash('No realizamos entregas los fines de semana. Por favor seleccione un día entre semana.', 'error')
                return render_template("cliente/menuCliente.html", 
                                    galletas=galletas_info,
                                    min_date=min_date.strftime('%Y-%m-%d'),
                                    max_date=max_date.strftime('%Y-%m-%d'),
                                    min_date_display=min_date_display,
                                    max_date_display=max_date_display)
            
            # Crear nuevo pedido
            nuevo_pedido = Pedidos(
                idClienteFK=session['user_id'],
                fechaPedido=datetime.now(),
                fechaEntrega=fecha_entrega,
                total=0,
                estado='Pendiente',
                observaciones=request.form.get('observaciones', '')
            )
            db.session.add(nuevo_pedido)
            db.session.flush()
            
            # Procesar detalles del pedido
            total = 0
            for galleta_id, presentacion_id in zip(
                request.form.getlist('galleta_id'), 
                request.form.getlist('presentacion_id')
            ):
                cantidad = int(request.form.get(f'cantidad_{galleta_id}_{presentacion_id}', 0))
                if cantidad > 0:
                    precio = PreciosGalletas.query.filter_by(
                        idGalletaFK=galleta_id,
                        idPresentacionFK=presentacion_id
                    ).first().precio
                    
                    subtotal = precio * cantidad
                    total += subtotal
                    
                    detalle = DetallePedido(
                        idPedidoFK=nuevo_pedido.idPedido,
                        idGalletaFK=galleta_id,
                        idPresentacionFK=presentacion_id,
                        cantidad=cantidad,
                        precioUnitario=precio,
                        subtotal=subtotal
                    )
                    db.session.add(detalle)
            
            # Actualizar total del pedido
            nuevo_pedido.total = total
            db.session.commit()
            
            flash('¡Pedido realizado con éxito!', 'success')
            return redirect(url_for('cliente.misPedidos'))
            
        except ValueError:
            flash('Formato de fecha inválido. Por favor use el selector de fecha.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al realizar el pedido: {str(e)}', 'error')
    
    return render_template("cliente/menuCliente.html", 
                         galletas=galletas_info,
                         min_date=min_date.strftime('%Y-%m-%d'),
                         max_date=max_date.strftime('%Y-%m-%d'),
                         min_date_display=min_date_display,
                         max_date_display=max_date_display)

@cliente_bp.route("/misPedidos")
@cliente_required
def misPedidos():
    pedidos = Pedidos.query.filter_by(idClienteFK=session['user_id'])\
                          .order_by(Pedidos.fechaPedido.desc())\
                          .all()
    return render_template("cliente/misPedidos.html", pedidos=pedidos)