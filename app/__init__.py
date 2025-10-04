import logging
from app.create_app.create_app import create_app
from app.create_app.create_migration_app import create_migration_app
from app.create_app.extensions import db, migrate, login

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('APP')

# Forces all models to be loaded
import app.models

