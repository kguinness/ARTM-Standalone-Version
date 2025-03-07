#from flask_sqlalchemy import SQLAlchemy
#from backend import db

#db = SQLAlchemy()  # ✅ Define db here and initialize it in create_app()

# Import models after defining db to avoid circular imports
from backend.models.user import User
from backend.models.gestures import Gesture
