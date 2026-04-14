from flask import Flask, session
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mysql.init_app(app)

    @app.context_processor
    def inject_usuario():
        try:
            from app.models.usuario import get_usuario_by_id
            uid = session.get('usuario_id')
            if not uid:
                return {'usuario_actual': None}
            usuario = get_usuario_by_id(uid)
            return {'usuario_actual': usuario}
        except Exception:
            return {'usuario_actual': None}

    from app.routes import main
    from app.routes.clases import clases_bp
    from app.routes.tareas import tareas_bp
    from app.routes.entregas import entregas_bp
    from app.routes.calificaciones import calificaciones_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main)
    app.register_blueprint(clases_bp)
    app.register_blueprint(tareas_bp)
    app.register_blueprint(entregas_bp)
    app.register_blueprint(calificaciones_bp)
    app.register_blueprint(auth_bp)

    return app
