from app import mysql

def calificar_entrega(entrega_id, nota, comentario):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO calificaciones (entrega_id, nota, comentario)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE nota = VALUES(nota), comentario = VALUES(comentario)
    """, (entrega_id, nota, comentario))
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
        SELECT t.titulo, t.id as tarea_id, c.nota, c.comentario
        FROM tareas t
        LEFT JOIN entregas e ON e.tarea_id = t.id AND e.alumno_id = %s
        LEFT JOIN calificaciones c ON c.entrega_id = e.id
        WHERE t.clase_id = %s
        ORDER BY t.fecha_limite ASC
    """, (alumno_id, clase_id))
    cals = cur.fetchall()
    cur.close()
    return cals
