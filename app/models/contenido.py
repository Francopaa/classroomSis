from app import mysql

def crear_contenido(titulo, archivo, clase_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO contenidos (titulo, archivo, clase_id) VALUES (%s, %s, %s)",
        (titulo, archivo, clase_id)
    )
    mysql.connection.commit()
    cur.close()

def get_contenidos_clase(clase_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM contenidos WHERE clase_id = %s ORDER BY creado_en DESC",
        (clase_id,)
    )
    contenidos = cur.fetchall()
    cur.close()
    return contenidos
