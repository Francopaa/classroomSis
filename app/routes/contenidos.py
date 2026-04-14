import os, uuid
from flask import Blueprint, request, redirect, url_for, current_app
from app.models.contenido import crear_contenido
from app.routes import get_usuario_actual

contenidos_bp = Blueprint('contenidos', __name__)

@contenidos_bp.route('/clases/<int:clase_id>/contenidos', methods=['POST'])
def subir(clase_id):
    titulo = request.form.get('titulo', '').strip() or 'Sin título'
    archivo = request.files.get('archivo')
    if not archivo or not archivo.filename.lower().endswith('.pdf'):
        return redirect(url_for('clases.detalle', clase_id=clase_id))
    nombre_archivo = f"{uuid.uuid4().hex}.pdf"
    archivo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_archivo))
    crear_contenido(titulo, nombre_archivo, clase_id)
    return redirect(url_for('clases.detalle', clase_id=clase_id))
