from config import SQLALCHEMY_DATABASE_URI
from website import db, app
import os.path

db.create_all()

