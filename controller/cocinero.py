from flask import Flask, render_template, request, Blueprint, jsonify, make_response
from models.models import db, Galletas, EstadoGalleta, MateriasPrimas, InventarioGalletas, IngredientesReceta
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from werkzeug.exceptions import BadRequest

chefCocinero = Blueprint('chefCocinero', __name__)

@chefCocinero.route('/produccion')
def produccion():
    galletas = (
        db.session.query(Galletas, EstadoGalleta.estatus)
        .join(EstadoGalleta, Galletas.idGalleta == EstadoGalleta.idGalletaFK)
        .all()
    )
    
    csrf_token = generate_csrf()  # Genera el token una sola vez
    response = make_response(render_template('produccion.html', galletas=galletas, csrf_token=csrf_token))
    response.set_cookie('csrf_token', csrf_token, httponly=True, samesite='Strict')  # Usa el mismo token
    
    return response



@chefCocinero.route('/actualizar_estado', methods=['POST'])
def actualizar_estado():
    try:
        # Validación CSRF (omitida por brevedad)
        data = request.get_json()
        id_galleta = int(data['idGalleta'])
        nuevo_estado = data['nuevo_estado']

        # 1. Actualizar estado de la galleta
        estado_galleta = EstadoGalleta.query.filter_by(idGalletaFK=id_galleta).first()
        if not estado_galleta:
            raise BadRequest(f"Galleta con ID {id_galleta} no encontrada")
        
        estado_galleta.estatus = nuevo_estado
        db.session.commit()

        # 2. Si el estado es "Aprobada", restar ingredientes del inventario
        if nuevo_estado == "Aprobada":
            # Obtener la receta asociada a la galleta
            galleta = Galletas.query.get(id_galleta)
            if not galleta:
                raise BadRequest(f"Galleta con ID {id_galleta} no encontrada")

            # Obtener todos los ingredientes de la receta
            ingredientes_receta = IngredientesReceta.query.filter_by(
                idRecetaFK=galleta.idRecetaFK
            ).all()

            for ingrediente in ingredientes_receta:
                # Verificar y actualizar inventario
                materia_prima = MateriasPrimas.query.get(ingrediente.idMateriaPrimaFK)
                if not materia_prima:
                    raise BadRequest(f"Materia prima con ID {ingrediente.idMateriaPrimaFK} no encontrada")

                if materia_prima.cantidadDisponible < ingrediente.cantidadNecesaria:
                    raise BadRequest(f"No hay suficiente {materia_prima.nombre} en inventario")

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