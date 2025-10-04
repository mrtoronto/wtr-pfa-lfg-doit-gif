import os
import time
import logging
from flask import Flask, request, g
from config import Config
from app.create_app.extensions import db, login, migrate, compress, cors

logger = logging.getLogger('APP')

def create_app(config_class=Config):
    """Creates the main Flask application with all configurations and routes."""
    logger.info(f'Starting up application in {os.environ.get("RUN_MODE", "dev")}...')
    start_time = time.time()
    
    # Get the absolute path to the app directory
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    app = Flask(__name__, 
                template_folder=os.path.join(app_dir, 'templates'),
                static_folder=os.path.join(app_dir, 'static'),
                static_url_path='/static')
    
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']
    
    # Initialize Flask extensions
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    compress.init_app(app)
    cors.init_app(app)
    
    # Setup user loader for Flask-Login
    from app.models.db.user import User
    
    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes.main_routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Add custom Jinja filters (optional)
    @app.template_filter('format_date')
    def format_date_filter(date_obj):
        if not date_obj:
            return ''
        return date_obj.strftime('%B %d, %Y')
    
    @app.before_request
    def before_request_func():
        """Start a timer at the beginning of a request."""
        if '/static' not in request.path:
            g.start_time = time.time()
    
    @app.after_request
    def after_request_func(response):
        """Calculate and log the time taken to process the request."""
        if 'start_time' in g:
            elapsed = time.time() - g.start_time
            if '/static' not in request.path:
                logger.debug(f"Request to {request.path} took {elapsed:.4f} seconds.")
        return response
    
    logger.info(f'Application started up in {time.time() - start_time:.4f} seconds')
    return app

