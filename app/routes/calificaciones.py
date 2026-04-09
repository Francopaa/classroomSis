from flask import Blueprint, request, jsonify
from app.models.calificacion import calificar_entrega, get_calificacion_by_entrega, get_calificaciones_alumno

calificaciones_bp = Blueprint('calificaciones', __name__)

@calificaciones_bp.route('/entregas/<int:entrega_id>/calificacion', methods=['POST'])
def calificar(entrega_id):
    data = request.json
    if not (0 <= float(data['nota']) <= 100):
        return jsonify({'error': 'La nota debe estar entre 0 y 100'}), 400
    calificar_entrega(entrega_id, data['nota'], data.get('comentario'))
    return jsonify({'mensaje': 'Calificación registrada'}), 201

@calificaciones_bp.route('/alumnos/<int:alumno_id>/clases/<int:clase_id>/calificaciones', methods=['GET'])
def listar_alumno(alumno_id, clase_id):
    cals = get_calificaciones_alumno(alumno_id, clase_id)
    return jsonify(cals)
