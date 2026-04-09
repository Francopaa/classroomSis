from flask import Blueprint, request, jsonify
from app.models.entrega import crear_entrega, get_entrega, get_entregas_tarea
from app.models.usuario import get_usuarios_clase

entregas_bp = Blueprint('entregas', __name__)

@entregas_bp.route('/tareas/<int:tarea_id>/entregas', methods=['POST'])
def entregar(tarea_id):
    data = request.json
    existente = get_entrega(data['alumno_id'], tarea_id)
    if existente:
        return jsonify({'error': 'Ya entregaste esta tarea'}), 400
    crear_entrega(data.get('contenido'), data.get('archivo'), data['alumno_id'], tarea_id)
    return jsonify({'mensaje': 'Entrega registrada exitosamente'}), 201

@entregas_bp.route('/tareas/<int:tarea_id>/entregas', methods=['GET'])
def listar(tarea_id):
    entregas = get_entregas_tarea(tarea_id)
    return jsonify(entregas)
