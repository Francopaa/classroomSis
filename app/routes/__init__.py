from flask import Blueprint, jsonify
from app import mysql

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({'mensaje': 'Classroom API corriendo correctamente'})

@main.route('/test-db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT 1')
        cur.close()
        return jsonify({'mensaje': 'Conexión a la base de datos exitosa'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
