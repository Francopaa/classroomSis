from flask import Blueprint, request, jsonify
from app.models.tarea import crear_tarea, get_tareas_clase, get_tarea_by_id

tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/clases/<int:clase_id>/tareas', methods=['POST'])
def crear(clase_id):
    data = request.json
    if not data.get('titulo') or not data.get('fecha_limite'):
        return jsonify({'error': 'Título y fecha límite son obligatorios'}), 400
    crear_tarea(data['titulo'], data.get('descripcion'), data['fecha_limite'], clase_id)
    return jsonify({'mensaje': 'Tarea creada'}), 201

@tareas_bp.route('/clases/<int:clase_id>/tareas', methods=['GET'])
def listar(clase_id):
    tareas = get_tareas_clase(clase_id)
    return jsonify(tareas)
