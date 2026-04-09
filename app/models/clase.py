from app import mysql
import random, string

def generar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def crear_clase(nombre, descripcion, profesor_id):
    codigo = generar_codigo()
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO clases (nombre, descripcion, codigo, profesor_id) VALUES (%s, %s, %s, %s)",
        (nombre, descripcion, codigo, profesor_id)
    )
    mysql.connection.commit()
    cur.close()
    return codigo

def get_clases_profesor(profesor_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clases WHERE profesor_id = %s", (profesor_id,))
    clases = cur.fetchall()
    cur.close()
    return clases

def get_clase_by_codigo(codigo):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clases WHERE codigo = %s", (codigo,))
    clase = cur.fetchone()
    cur.close()
    return clase

def unirse_a_clase(clase_id, alumno_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO clase_alumnos (clase_id, alumno_id) VALUES (%s, %s)",
        (clase_id, alumno_id)
    )
    mysql.connection.commit()
    cur.close()

def get_clases_alumno(alumno_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.* FROM clases c
        JOIN clase_alumnos ca ON c.id = ca.clase_id
        WHERE ca.alumno_id = %s
    """, (alumno_id,))
    clases = cur.fetchall()
    cur.close()
    return clases
