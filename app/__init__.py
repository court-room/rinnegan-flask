import os

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app import config


db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()
migrate = Migrate()
