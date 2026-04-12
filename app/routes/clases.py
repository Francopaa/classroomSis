from flask import Blueprint, request, render_template, redirect, url_for

clases_bp = Blueprint('clases', __name__)

@clases_bp.route('/clases/crear', methods=['GET'])
def crear_form():
    return render_template('clases/crear.html')

@clases_bp.route('/clases', methods=['POST'])
def crear():
    return redirect(url_for('main.index'))

@clases_bp.route('/clases/unirse', methods=['GET'])
def unirse_form():
    return render_template('clases/unirse.html')

@clases_bp.route('/clases/unirse', methods=['POST'])
def unirse():
    return redirect(url_for('main.index'))

@clases_bp.route('/clases/<int:clase_id>', methods=['GET'])
def detalle(clase_id):
    clase = {'id': clase_id, 'nombre': 'Clase de prueba', 'descripcion': 'Descripción de prueba'}
    return render_template('tareas/listado.html', clase=clase, tareas=[], es_profesor=True)