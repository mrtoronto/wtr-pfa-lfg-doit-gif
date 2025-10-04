from flask import Flask
from config import Config
from app.create_app.extensions import db, migrate

def create_migration_app(config_class=Config):
    """Creates a Flask application configured for database migrations."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    return app

