from flask import Blueprint, request, render_template, redirect, url_for
  from app.models.calificacion import calificar_entrega, get_calificacion_by_entrega, get_calificaciones_alumno                                      
  from app.models.entrega import get_entrega_by_id                                                                                                   
  from app.models.tarea import get_tarea_by_id
  from app.models.clase import get_clase_by_id                                                                                                       
  from app.routes import get_usuario_actual                 
                                                                                                                                                     
  calificaciones_bp = Blueprint('calificaciones', _name_) 

  @calificaciones_bp.route('/entregas/<int:entrega_id>/calificar', methods=['GET'])                                                                  
  def calificar_form(entrega_id):
      entrega = get_entrega_by_id(entrega_id)                                                                                                        
      tarea = get_tarea_by_id(entrega['tarea_id'])          
      calificacion = get_calificacion_by_entrega(entrega_id)                                                                                         
      return render_template('calificaciones/calificar.html',
          entrega=entrega, tarea=tarea, calificacion=calificacion)                                                                                   
                                                                                                                                                     
  @calificaciones_bp.route('/entregas/<int:entrega_id>/calificacion', methods=['POST'])
  def calificar(entrega_id):                                                                                                                         
      nota = request.form.get('nota')                                                                                                                
      comentario = request.form.get('comentario')
      if not nota or not (0 <= float(nota) <= 100):                                                                                                  
          return redirect(url_for('calificaciones.calificar_form', entrega_id=entrega_id))
      calificar_entrega(entrega_id, float(nota), comentario)                                                                                         
      entrega = get_entrega_by_id(entrega_id)
      return redirect(url_for('entregas.listado', tarea_id=entrega['tarea_id']))                                                                     
                                                            
  @calificaciones_bp.route('/clases/<int:clase_id>/mis-calificaciones', methods=['GET'])                                                             
  def mis_calificaciones(clase_id):                         
      usuario = get_usuario_actual()                                                                                                                 
      clase = get_clase_by_id(clase_id)                     
      calificaciones = get_calificaciones_alumno(usuario['id'], clase_id)
      return render_template('calificaciones/mis_calificaciones.html',                                                                               
          calificaciones=calificaciones, clase=clase)
