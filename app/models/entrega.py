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
