from app import mysql

def calificar_entrega(entrega_id, nota, comentario):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO calificaciones (entrega_id, nota, comentario) VALUES (%s, %s, %s)",
        (entrega_id, nota, comentario)
    )
    mysql.connection.commit()
    cur.close()

def get_calificacion_by_entrega(entrega_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM calificaciones WHERE entrega_id = %s", (entrega_id,))
    cal = cur.fetchone()
    cur.close()
    return cal

def get_calificaciones_alumno(alumno_id, clase_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT t.titulo, c.nota, c.comentario
        FROM calificaciones c
        JOIN entregas e ON c.entrega_id = e.id
        JOIN tareas t ON e.tarea_id = t.id
        WHERE e.alumno_id = %s AND t.clase_id = %s
    """, (alumno_id, clase_id))
    cals = cur.fetchall()
    cur.close()
    return cals
