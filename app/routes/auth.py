from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.usuario import get_usuario_by_email, crear_usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('usuario_id'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Completa todos los campos.', 'error')
            return render_template('auth/login.html')

        usuario = get_usuario_by_email(email)
        if not usuario:
            flash('Correo o contraseña incorrectos.', 'error')
            return render_template('auth/login.html')

        if not check_password_hash(usuario['password'], password):
            flash('Correo o contraseña incorrectos.', 'error')
            return render_template('auth/login.html')

        session['usuario_id'] = usuario['id']
        return redirect(url_for('main.index'))

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('usuario_id'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirmar = request.form.get('confirmar', '')
        rol = request.form.get('rol', 'alumno')

        if not nombre or not email or not password or not confirmar:
            flash('Completa todos los campos.', 'error')
            return render_template('auth/register.html')

        if password != confirmar:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('auth/register.html')

        if rol not in ('profesor', 'alumno'):
            rol = 'alumno'

        if get_usuario_by_email(email):
            flash('Ya existe una cuenta con ese correo.', 'error')
            return render_template('auth/register.html')

        hashed = generate_password_hash(password)
        crear_usuario(nombre, email, hashed, rol)

        flash('Cuenta creada. Inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
