from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mysql.init_app(app)

    # Registrar blueprints
    from app.routes import main
    from app.routes.clases import clases_bp
    from app.routes.tareas import tareas_bp
    from app.routes.entregas import entregas_bp
    from app.routes.calificaciones import calificaciones_bp

    app.register_blueprint(main)
    app.register_blueprint(clases_bp)
    app.register_blueprint(tareas_bp)
    app.register_blueprint(entregas_bp)
    app.register_blueprint(calificaciones_bp)

    return app
