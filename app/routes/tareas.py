from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models.tarea import crear_tarea, get_tareas_clase, get_tarea_by_id

tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/clases/<int:clase_id>/tareas/crear', methods=['GET'])
def crear_form(clase_id):
    clase = {'id': clase_id, 'nombre': 'Clase de prueba', 'descripcion': 'Descripción de prueba'}
    return render_template('tareas/crear.html', clase=clase)

@tareas_bp.route('/clases/<int:clase_id>/tareas', methods=['POST'])
def crear(clase_id):
    if request.is_json:
        data = request.json
    else:
        data = request.form
    if not data.get('titulo') or not data.get('fecha_limite'):
        if request.is_json:
            return jsonify({'error': 'Título y fecha límite son obligatorios'}), 400
        return redirect(url_for('tareas.crear_form', clase_id=clase_id))
    crear_tarea(data['titulo'], data.get('descripcion'), data['fecha_limite'], clase_id)
    if request.is_json:
        return jsonify({'mensaje': 'Tarea creada'}), 201
    return redirect(url_for('clases.detalle', clase_id=clase_id))

@tareas_bp.route('/clases/<int:clase_id>/tareas', methods=['GET'])
def listar(clase_id):
    tareas = get_tareas_clase(clase_id)
    return jsonify(tareas)

@tareas_bp.route('/tareas/<int:tarea_id>', methods=['GET'])
def detalle(tarea_id):
    tarea = get_tarea_by_id(tarea_id)
    return render_template('tareas/detalle.html', tarea=tarea)
