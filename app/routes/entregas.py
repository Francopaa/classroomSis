from flask import Blueprint, request, render_template, redirect, url_for                                                                           
  from app.routes import get_usuario_actual                                                                                                          
  from app.models.entrega import crear_entrega, get_entrega                                                                                          
  from app.models.tarea import get_tarea_by_id                                                                                                       
  from app.models.clase import get_clase_by_id                                                                                                       
                                                                                                                                                     
  entregas_bp = Blueprint('entregas', __name__)                                                                                                      
   
  @entregas_bp.route('/tareas/<int:tarea_id>/entregar', methods=['GET'])                                                                             
  def entregar_form(tarea_id):                              
      usuario = get_usuario_actual()
      tarea = get_tarea_by_id(tarea_id)
      clase = get_clase_by_id(tarea['clase_id'])                                                                                                     
      entrega = get_entrega(usuario['id'], tarea_id)
      return render_template('entregas/entregar.html', tarea=tarea, clase=clase, entrega=entrega)                                                    
                                                                                                                                                     
  @entregas_bp.route('/tareas/<int:tarea_id>/entregas', methods=['POST'])                                                                            
  def entregar(tarea_id):                                                                                                                            
      usuario = get_usuario_actual()                                                                                                                 
      existente = get_entrega(usuario['id'], tarea_id)      
      if not existente:                                                                                                                              
          crear_entrega(
              request.form.get('contenido'),                                                                                                         
              request.form.get('archivo'),                  
              usuario['id'],
              tarea_id                                                                                                                               
          )
      return redirect(url_for('entregas.entregar_form', tarea_id=tarea_id))
