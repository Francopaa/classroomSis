from app import mysql

def crear_tarea(titulo, descripcion, fecha_limite, clase_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO tareas (titulo, descripcion, fecha_limite, clase_id) VALUES (%s, %s, %s, %s)",
        (titulo, descripcion, fecha_limite, clase_id)
    )
    mysql.connection.commit()
    cur.close()

def get_tareas_clase(clase_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM tareas WHERE clase_id = %s ORDER BY fecha_limite ASC",
        (clase_id,)
    )
    tareas = cur.fetchall()
    cur.close()
    return tareas

def get_tarea_by_id(tarea_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tareas WHERE id = %s", (tarea_id,))
    tarea = cur.fetchone()
    cur.close()
    return tarea
