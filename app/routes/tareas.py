from flask import Blueprint, request, render_template, redirect, url_for
from app.routes import get_usuario_actual
from app.models.tarea import crear_tarea, get_tarea_by_id
from app.models.clase import get_clase_by_id
from app.models.entrega import get_entrega
from app.models.calificacion import get_calificacion_by_entrega

tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/clases/<int:clase_id>/tareas/crear', methods=['GET'])
def crear_form(clase_id):
    clase = get_clase_by_id(clase_id)
    return render_template('tareas/crear.html', clase=clase)

@tareas_bp.route('/clases/<int:clase_id>/tareas', methods=['POST'])
def crear(clase_id):
    data = request.form
    if not data.get('titulo') or not data.get('fecha') or not data.get('hora'):
        return redirect(url_for('tareas.crear_form', clase_id=clase_id))
    fecha_limite = data['fecha'] + ' ' + data['hora']
    crear_tarea(data['titulo'], data.get('descripcion'), fecha_limite, clase_id)
    return redirect(url_for('clases.detalle', clase_id=clase_id))

@tareas_bp.route('/tareas/<int:tarea_id>', methods=['GET'])
def detalle(tarea_id):
    usuario = get_usuario_actual()
    tarea = get_tarea_by_id(tarea_id)
    if not tarea:
        return render_template('tareas/detalle.html', tarea=None)
    clase = get_clase_by_id(tarea['clase_id'])
    es_profesor = clase['profesor_id'] == usuario['id']

    entrega = None
    calificacion = None
    if not es_profesor:
        entrega = get_entrega(usuario['id'], tarea_id)
        if entrega:
            calificacion = get_calificacion_by_entrega(entrega['id'])

    return render_template('tareas/detalle.html',
        tarea=tarea, clase=clase, es_profesor=es_profesor,
        entrega=entrega, calificacion=calificacion)
