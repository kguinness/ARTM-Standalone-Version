#from flask import Blueprint
from backend.routes.gesture_routes import bp as gesture_bp
from backend.routes.user_routes import bp as user_bp


# Register all blueprints here
def register_blueprints(app):
    app.register_blueprint(gesture_bp, url_prefix="/gestures")
    app.register_blueprint(user_bp, url_prefix="/users")




