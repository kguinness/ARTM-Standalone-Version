from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from backend.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["DEBUG"] = True

    db.init_app(app)
    bcrypt.init_app(app)


    from backend.models.user import User
    from backend.models.gestures import Gesture
    from backend.routes.user_routes import bp as user_bp
    from backend.routes.gesture_routes import bp as gesture_bp


    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(gesture_bp)
    #, url_prefix="/gestures"

    Migrate(app, db)

    # Register blueprints
    with app.app_context():
        db.create_all()


    # Store the latest recognized gesture to display in backend log
    app.config["LATEST_GESTURE"] = "No gestures detected yet."

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.route('/update_gesture', methods=['POST'])
    def update_gesture():
        data = request.json
        if "gesture" in data:
            app.config["LATEST_GESTURE"] = data["gesture"]
            return jsonify({"status": "success", "message": "Latest gesture updated."})
        return jsonify({"status": "error", "message": "No gesture provided."}), 400

    @app.route('/')
    def home():
        return jsonify({
            "message": "Flask backend is running!",
            "latest_gesture": app.config["LATEST_GESTURE"],
            "most_latest_gesture": "test"
        })

    return app
