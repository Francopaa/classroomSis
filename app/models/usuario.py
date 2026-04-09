from app import mysql

def get_usuario_by_email(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cur.fetchone()
    cur.close()
    return usuario

def crear_usuario(nombre, email, password, rol):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)",
        (nombre, email, password, rol)
    )
    mysql.connection.commit()
    cur.close()

def get_usuarios_clase(clase_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT u.id, u.nombre, u.email FROM usuarios u
        JOIN clase_alumnos ca ON u.id = ca.alumno_id
        WHERE ca.clase_id = %s
    """, (clase_id,))
    usuarios = cur.fetchall()
    cur.close()
    return usuarios
