import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger('APP')
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))

class Config(object):
    # Import from local_settings.py (not in git)
    try:
        import local_settings
        SECRET_KEY = local_settings.SECRET_KEY
        DATABASE_URL_FROM_SETTINGS = getattr(local_settings, 'DATABASE_URL', None)
    except ImportError:
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
        DATABASE_URL_FROM_SETTINGS = None
    
    RUN_MODE = os.environ.get('RUN_MODE') or 'dev'
    logger.info(f'RUN_MODE: {RUN_MODE}')
    
    # Database configuration
    if RUN_MODE == 'dev':
        SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'dev.db')
        SERVER_NAME = '127.0.0.1:5000'
        PREFERRED_URL_SCHEME = 'http'
    elif RUN_MODE == 'prod':
        SQLALCHEMY_DATABASE_URI = DATABASE_URL_FROM_SETTINGS or os.environ.get('DATABASE_URL')
        SERVER_NAME = os.environ.get('SERVER_NAME')  # Optional, leave None for IP-based access
        PREFERRED_URL_SCHEME = 'http'  # Use https when you have SSL
    elif RUN_MODE == 'test':
        SQLALCHEMY_DATABASE_URI = 'sqlite://'  # In-memory database
        SERVER_NAME = 'localhost:5000'
        PREFERRED_URL_SCHEME = 'http'
        TESTING = True
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Optional: Admin emails for error notifications
    ADMINS = [os.environ.get('ADMIN_EMAIL', 'admin@example.com')]
