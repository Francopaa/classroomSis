from flask import Blueprint, request, render_template, redirect, url_for
from app.routes import get_usuario_actual
from app.models.clase import crear_clase, get_clase_by_id, get_clase_by_codigo, unirse_a_clase
from app.models.tarea import get_tareas_clase
from app.models.entrega import get_entrega

clases_bp = Blueprint('clases', __name__)

@clases_bp.route('/clases/crear', methods=['GET'])
def crear_form():
    return render_template('clases/crear.html')

@clases_bp.route('/clases', methods=['POST'])
def crear():
    usuario = get_usuario_actual()
    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    if not nombre:
        return redirect(url_for('clases.crear_form'))
    crear_clase(nombre, descripcion or None, usuario['id'])
    return redirect(url_for('main.index'))

@clases_bp.route('/clases/unirse', methods=['GET'])
def unirse_form():
    return render_template('clases/unirse.html')

@clases_bp.route('/clases/unirse', methods=['POST'])
def unirse():
    usuario = get_usuario_actual()
    codigo = request.form.get('codigo', '').strip().upper()
    if not codigo:
        return render_template('clases/unirse.html', error='Ingresa un código')
    clase = get_clase_by_codigo(codigo)
    if not clase:
        return render_template('clases/unirse.html', error='Código inválido')
    unirse_a_clase(clase['id'], usuario['id'])
    return redirect(url_for('clases.detalle', clase_id=clase['id']))

@clases_bp.route('/clases/<int:clase_id>', methods=['GET'])
def detalle(clase_id):
    usuario = get_usuario_actual()
    clase = get_clase_by_id(clase_id)
    if not clase:
        return redirect(url_for('main.index'))
    es_profesor = clase['profesor_id'] == usuario['id']
    tareas_raw = get_tareas_clase(clase_id)
    tareas = []
    for t in tareas_raw:
        tarea = dict(t)
        if not es_profesor:
            tarea['entregada'] = bool(get_entrega(usuario['id'], t['id']))
        tareas.append(tarea)
    return render_template('clases/detalle.html', clase=clase, tareas=tareas, es_profesor=es_profesor)
