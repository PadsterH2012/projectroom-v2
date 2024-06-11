from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        # Import routes here to avoid circular imports
        from .routes import main_routes
        app.register_blueprint(main_routes)
    
    return app
