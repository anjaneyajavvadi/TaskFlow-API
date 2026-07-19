from flask import Flask
from app.config import Config
from app.extensions import db,migrate,jwt,ma

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    ma.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.tasks import task_bp

    app.register_blueprint(auth_bp,url_prefix="/api/auth")
    app.register_blueprint(task_bp,url_prefix="/api/tasks")    

    return app