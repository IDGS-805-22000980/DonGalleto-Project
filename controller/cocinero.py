from flask import Flask, render_template, request, Blueprint, jsonify, make_response
from models.models import db, Galletas, EstadoGalleta
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
    
    response = make_response(render_template('produccion.html', galletas=galletas, csrf_token=generate_csrf()))
    response.set_cookie('csrf_token', generate_csrf(), httponly=True, samesite='Strict')
    return response



@chefCocinero.route('/actualizar_estado', methods=['POST'])
def actualizar_estado():
    try:
        csrf_token = request.headers.get('X-CSRFToken') or request.json.get('csrf_token')
        if not csrf_token:
            return jsonify({"error": "Token CSRF faltante"}), 400
        validate_csrf(csrf_token)
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibieron datos JSON"}), 400
        required_fields = ['idGalleta', 'nuevo_estado']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Datos incompletos"}), 400
        id_galleta = int(data['idGalleta'])
        nuevo_estado = data['nuevo_estado']
        if nuevo_estado not in ["Pendiente", "Aprobada", "Rechazada", "Completada"]:
            return jsonify({"error": "Estado no válido"}), 400
        estado_galleta = EstadoGalleta.query.filter_by(idGalletaFK=id_galleta).first()
        if not estado_galleta:
            return jsonify({"error": f"Galleta con ID {id_galleta} no encontrada"}), 404
        estado_galleta.estatus = nuevo_estado
        db.session.commit()
        return jsonify({
            "message": "Estado actualizado", 
            "nuevo_estado": nuevo_estado,
            "csrf_token": generate_csrf()
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error interno: {str(e)}")  # Esto mostrará el error en la consola
        return jsonify({"error": "Error interno del servidor"}), 500
