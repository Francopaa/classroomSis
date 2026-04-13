from flask import Blueprint, render_template, session, redirect, url_for
  from app.models.usuario import get_usuario_by_id
  from app.models.clase import get_clases_profesor, get_clases_alumno

  main = Blueprint('main', __name__)

  def get_usuario_actual():
      uid = session.get('usuario_id', 1)
      return get_usuario_by_id(uid)

  @main.route('/')
  def index():
      usuario = get_usuario_actual()
      if usuario['rol'] == 'profesor':
          clases = get_clases_profesor(usuario['id'])
      else:
          clases = get_clases_alumno(usuario['id'])
      return render_template('index.html', clases=clases, usuario=usuario)

  @main.route('/dev/switch/<int:uid>')
  def switch_user(uid):
      session['usuario_id'] = uid
      return redirect(url_for('main.index'))
