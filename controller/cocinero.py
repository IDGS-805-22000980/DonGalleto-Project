from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, make_response
from models.models import db, Galletas, EstadoGalleta, MateriasPrimas, InventarioGalletas, IngredientesReceta
from flask_wtf.csrf import generate_csrf
from werkzeug.exceptions import BadRequest

chefCocinero = Blueprint('chefCocinero', __name__)

@chefCocinero.route('/produccion')
def produccion():
    galletas = (
        db.session.query(Galletas, EstadoGalleta.estatus)
        .join(EstadoGalleta, Galletas.idGalleta == EstadoGalleta.idGalletaFK)
        .join(InventarioGalletas, Galletas.idGalleta == InventarioGalletas.idGalletaFK)
        .filter(InventarioGalletas.stock < 50)
        .with_entities(Galletas, EstadoGalleta.estatus)
        .all()
    )

    csrf_token = generate_csrf()
    response = make_response(render_template('produccion.html', galletas=galletas, csrf_token=csrf_token))
    response.set_cookie('csrf_token', csrf_token, httponly=True, samesite='Strict')

    return response


@chefCocinero.route('/actualizar_estado', methods=['POST'])
def actualizar_estado():
    try:
        data = request.get_json()
        id_galleta = int(data['idGalleta'])
        nuevo_estado = data['nuevo_estado']

        estado_galleta = EstadoGalleta.query.filter_by(idGalletaFK=id_galleta).first()
        if not estado_galleta:
            raise BadRequest(f"Galleta con ID {id_galleta} no encontrada")
        
        estado_galleta.estatus = nuevo_estado

        # Si el estado es "Aprobada", verificar stock de ingredientes antes de restar
        if nuevo_estado == "Aprobada":
            galleta = Galletas.query.get(id_galleta)
            if not galleta:
                raise BadRequest(f"Galleta con ID {id_galleta} no encontrada")

            ingredientes_receta = IngredientesReceta.query.filter_by(idRecetaFK=galleta.idRecetaFK).all()
            
            # Primero verificamos si hay suficiente stock
            for ingrediente in ingredientes_receta:
                materia_prima = MateriasPrimas.query.get(ingrediente.idMateriaPrimaFK)
                if materia_prima.cantidadDisponible < ingrediente.cantidadNecesaria:
                    raise BadRequest(f"No hay suficiente {materia_prima.nombre} en inventario")

            # Si hay suficiente stock, restamos los ingredientes
            for ingrediente in ingredientes_receta:
                materia_prima = MateriasPrimas.query.get(ingrediente.idMateriaPrimaFK)
                materia_prima.cantidadDisponible -= ingrediente.cantidadNecesaria

        db.session.commit()

        return jsonify({
            "message": "Estado actualizado",
            "nuevo_estado": nuevo_estado,
            "csrf_token": generate_csrf()
        }), 200

    except BadRequest as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error interno: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500


@chefCocinero.route('/guardar_cantidad', methods=['POST'])
def guardar_cantidad():
    try:
        data = request.get_json()
        id_galleta = int(data['idGalleta'])
        cantidad = int(data['cantidad'])

        galleta = Galletas.query.get(id_galleta)
        if not galleta:
            raise BadRequest(f"Galleta con ID {id_galleta} no encontrada")

        inventario = InventarioGalletas.query.filter_by(idGalletaFK=id_galleta, disponible=True).first()

        if not inventario:
            inventario = InventarioGalletas(
                idGalletaFK=id_galleta,
                stock=cantidad,
                fechaProduccion=datetime.today(),
                fechaCaducidad=datetime.today() + timedelta(days=365),
                lote=f"Lote-{id_galleta}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            )
            db.session.add(inventario)
        else:
            inventario.stock += cantidad

        # Cambiar estado a "Pendiente"
        estado_galleta = EstadoGalleta.query.filter_by(idGalletaFK=id_galleta).first()
        if estado_galleta:
            estado_galleta.estatus = "Pendiente"

        db.session.commit()

        return jsonify({
            "message": "Cantidad guardada",
            "csrf_token": generate_csrf()
        }), 200

    except BadRequest as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error interno: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500
