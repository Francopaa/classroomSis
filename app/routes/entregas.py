import os
from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, send_from_directory, current_app, flash
from app.routes import get_usuario_actual, login_required
from app.models.entrega import crear_entrega, get_entrega, get_alumnos_con_entrega
from app.models.tarea import get_tarea_by_id
from app.models.clase import get_clase_by_id

entregas_bp = Blueprint('entregas', __name__)

@entregas_bp.route('/tareas/<int:tarea_id>/entregar', methods=['GET'])
@login_required
def entregar_form(tarea_id):
    usuario = get_usuario_actual()
    tarea = get_tarea_by_id(tarea_id)
    clase = get_clase_by_id(tarea['clase_id'])
    entrega = get_entrega(usuario['id'], tarea_id)
    return render_template('entregas/entregar.html', tarea=tarea, clase=clase, entrega=entrega)

@entregas_bp.route('/tareas/<int:tarea_id>/entregas', methods=['POST'])
@login_required
def entregar(tarea_id):
    usuario = get_usuario_actual()
    tarea = get_tarea_by_id(tarea_id)
    if tarea['fecha_limite'] and datetime.now() > tarea['fecha_limite']:
        flash('El plazo de entrega ya venció.', 'error')
        return redirect(url_for('entregas.entregar_form', tarea_id=tarea_id))
    existente = get_entrega(usuario['id'], tarea_id)
    if not existente:
        nombre_archivo = None
        file = request.files.get('archivo')
        if file and file.filename:
            upload_dir = os.path.join(current_app.root_path, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            nombre_archivo = f"{usuario['id']}_{tarea_id}_{file.filename}"
            file.save(os.path.join(upload_dir, nombre_archivo))
        crear_entrega(
            request.form.get('contenido'),
            nombre_archivo,
            usuario['id'],
            tarea_id
        )
    return redirect(url_for('entregas.entregar_form', tarea_id=tarea_id))

@entregas_bp.route('/uploads/<path:filename>')
def descargar(filename):
    upload_dir = os.path.join(current_app.root_path, 'uploads')
    return send_from_directory(upload_dir, filename)

@entregas_bp.route('/tareas/<int:tarea_id>/entregas', methods=['GET'])
@login_required
def listado(tarea_id):
    tarea = get_tarea_by_id(tarea_id)
    clase = get_clase_by_id(tarea['clase_id'])
    alumnos = get_alumnos_con_entrega(tarea_id, clase['id'])

    alumnos_entregaron = []
    alumnos_pendientes = []
    for a in alumnos:
        if a['entrega_id']:
            alumnos_entregaron.append({
                'id': a['entrega_id'],
                'alumno_nombre': a['nombre'],
                'entregado_en': a['entregado_en'],
                'calificada': a['nota'] is not None,
                'nota': a['nota']
            })
        else:
            alumnos_pendientes.append({'nombre': a['nombre']})

    return render_template('entregas/listado.html',
        tarea=tarea, clase=clase,
        alumnos_entregaron=alumnos_entregaron,
        alumnos_pendientes=alumnos_pendientes)
