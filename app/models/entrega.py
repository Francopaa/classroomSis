from app import mysql

def crear_entrega(contenido, archivo, alumno_id, tarea_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO entregas (contenido, archivo, alumno_id, tarea_id) VALUES (%s, %s, %s, %s)",
        (contenido, archivo, alumno_id, tarea_id)
    )
    mysql.connection.commit()
    cur.close()

def get_entrega(alumno_id, tarea_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM entregas WHERE alumno_id = %s AND tarea_id = %s",
        (alumno_id, tarea_id)
    )
    entrega = cur.fetchone()
    cur.close()
    return entrega

def get_entrega_by_id(entrega_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT e.*, u.nombre as alumno_nombre
        FROM entregas e
        JOIN usuarios u ON e.alumno_id = u.id
        WHERE e.id = %s
    """, (entrega_id,))
    entrega = cur.fetchone()
    cur.close()
    return entrega

def get_entregas_tarea(tarea_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT e.*, u.nombre as alumno_nombre
        FROM entregas e
        JOIN usuarios u ON e.alumno_id = u.id
        WHERE e.tarea_id = %s
    """, (tarea_id,))
    entregas = cur.fetchall()
    cur.close()
    return entregas

def get_alumnos_con_entrega(tarea_id, clase_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT u.id as alumno_id, u.nombre,
               e.id as entrega_id, e.entregado_en,
               c.nota, c.comentario
        FROM clase_alumnos ca
        JOIN usuarios u ON ca.alumno_id = u.id
        LEFT JOIN entregas e ON e.alumno_id = u.id AND e.tarea_id = %s
        LEFT JOIN calificaciones c ON c.entrega_id = e.id
        WHERE ca.clase_id = %s
        ORDER BY u.nombre ASC
    """, (tarea_id, clase_id))
    resultado = cur.fetchall()
    cur.close()
    return resultado
