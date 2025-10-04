import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_compress import Compress
from flask_cors import CORS
from sqlalchemy import MetaData

# Setup database with naming convention
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

# Initialize Flask extensions
migrate = Migrate(db=db)
login = LoginManager()
login.login_view = 'main.login'
login.login_message = 'Please log in to see this page.'
compress = Compress()
cors = CORS()

