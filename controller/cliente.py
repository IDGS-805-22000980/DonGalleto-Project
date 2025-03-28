from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models.models import db, Usuario, Pedido, DetallePedido, Galleta, SeguimientoPedido
from datetime import datetime
from werkzeug.security import check_password_hash
from models.formsLogin import LoginForm
import models.forms
from controller.auth import cliente_required

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route("/menuCliente", methods=["GET", "POST"])
@cliente_required
def menuCliente():
    galletas = Galleta.query.all()
    return render_template("menuCliente.html", galletas=galletas)

@cliente_bp.route("/agregar_al_carrito", methods=["POST"])
@cliente_required
def agregar_al_carrito():
    try:
        # Verificar y obtener datos JSON
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 415
        
        data = request.get_json()
        galleta_id = data.get('galleta_id')
        cantidad = int(data.get('cantidad', 1))
        tipo_precio = data.get('tipo_precio', 'pieza')
        
        # Validar datos
        if not galleta_id:
            return jsonify({'success': False, 'error': 'Missing galleta_id'}), 400
        
        # Inicializar carrito si no existe
        if 'carrito' not in session:
            session['carrito'] = []
        
        # Buscar galleta en la base de datos
        galleta = Galleta.query.get(galleta_id)
        if not galleta:
            return jsonify({'success': False, 'error': 'Galleta no encontrada'}), 404
        
        # Determinar precio según tipo
        precio = float(galleta.precio_por_pieza if tipo_precio == 'pieza' else galleta.precio_por_gramo)
        
        # Buscar si ya existe en el carrito
        carrito = session['carrito']
        item_existente = next(
            (item for item in carrito 
             if item['galleta_id'] == galleta_id and item['tipo_precio'] == tipo_precio), 
            None
        )
        
        # Actualizar o agregar item
        if item_existente:
            item_existente['cantidad'] += cantidad
        else:
            carrito.append({
                'galleta_id': galleta.id_galleta,
                'nombre': galleta.nombre,
                'precio': precio,
                'tipo_precio': tipo_precio,
                'cantidad': cantidad
            })
        
        # Guardar en sesión
        session['carrito'] = carrito
        session.modified = True
        
        return jsonify({
            'success': True, 
            'carrito': session['carrito'],
            'total': sum(item['precio'] * item['cantidad'] for item in session['carrito'])
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
    data = request.get_json()
    # Resto del código igual que tienes actualmente...
    return jsonify({'success': True, 'carrito': session['carrito']})

@cliente_bp.route("/realizar_pedido", methods=["POST"])
@cliente_required
def realizar_pedido():
    if 'carrito' not in session or not session['carrito']:
        flash('El carrito está vacío', 'danger')
        return redirect(url_for('cliente.menuCliente'))
    
    try:
        # Crear el pedido principal
        nuevo_pedido = Pedido(
            idUsuario=session['user_id'],
            estado='Pendiente',
            direccionEntrega=request.form['direccion'],
            telefonoContacto=request.form['telefono'],
            notas=request.form.get('notas', ''),
            total=sum(item['precio'] * item['cantidad'] for item in session['carrito'])
        )
        db.session.add(nuevo_pedido)
        db.session.flush()  # Para obtener el ID del pedido
        
        # Agregar detalles del pedido
        for item in session['carrito']:
            detalle = DetallePedido(
                idPedido=nuevo_pedido.idPedido,
                idGalleta=item['galleta_id'],
                cantidad=item['cantidad'],
                precioUnitario=item['precio'],
                subtotal=item['precio'] * item['cantidad']
            )
            db.session.add(detalle)
        
        # Registrar el estado inicial
        seguimiento = SeguimientoPedido(
            idPedido=nuevo_pedido.idPedido,
            estadoNuevo='Pendiente',
            idUsuarioCambio=session['user_id'],
            comentarios='Pedido creado por el cliente'
        )
        db.session.add(seguimiento)
        
        db.session.commit()
        session.pop('carrito', None)
        
        flash('¡Pedido realizado con éxito!', 'success')
        return redirect(url_for('cliente.mis_pedidos'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al realizar el pedido: {str(e)}', 'danger')
        return redirect(url_for('cliente.menuCliente'))

@cliente_bp.route("/mis_pedidos")
@cliente_required
def mis_pedidos():
    pedidos = Pedido.query.filter_by(idUsuario=session['user_id']).order_by(Pedido.fechaPedido.desc()).all()
    return render_template("mis_pedidos.html", pedidos=pedidos)

@cliente_bp.route("/obtener_carrito", methods=["GET"])
@cliente_required
def obtener_carrito():
    return jsonify(session.get('carrito', []))

@cliente_bp.route("/eliminar_del_carrito", methods=["DELETE, POST"])
@cliente_required
def eliminar_del_carrito():
    if 'carrito' not in session:
        return jsonify({'success': False})
    
    data = request.get_json()
    galleta_id = data['galleta_id']
    tipo_precio = data['tipo_precio']
    
    session['carrito'] = [
        item for item in session['carrito'] 
        if not (item['galleta_id'] == galleta_id and item['tipo_precio'] == tipo_precio)
    ]
    session.modified = True
    return jsonify({'success': True, 'carrito': session['carrito']})