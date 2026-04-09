from flask import Blueprint, request, jsonify
from app.models.clase import crear_clase, get_clases_profesor, get_clase_by_codigo, unirse_a_clase, get_clases_alumno

clases_bp = Blueprint('clases', __name__)

@clases_bp.route('/clases', methods=['POST'])
def crear():
    data = request.json
    codigo = crear_clase(data['nombre'], data.get('descripcion'), data['profesor_id'])
    return jsonify({'mensaje': 'Clase creada', 'codigo': codigo}), 201

@clases_bp.route('/clases/profesor/<int:profesor_id>', methods=['GET'])
def listar_profesor(profesor_id):
    clases = get_clases_profesor(profesor_id)
    return jsonify(clases)

@clases_bp.route('/clases/unirse', methods=['POST'])
def unirse():
    data = request.json
    clase = get_clase_by_codigo(data['codigo'])
    if not clase:
        return jsonify({'error': 'Código inválido'}), 404
    unirse_a_clase(clase['id'], data['alumno_id'])
    return jsonify({'mensaje': 'Te uniste a la clase', 'clase': clase}), 200

@clases_bp.route('/clases/alumno/<int:alumno_id>', methods=['GET'])
def listar_alumno(alumno_id):
    clases = get_clases_alumno(alumno_id)
    return jsonify(clases)
