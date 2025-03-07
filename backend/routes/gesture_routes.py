from flask import Blueprint, request, jsonify, current_app, url_for
import requests

bp = Blueprint('gestures', __name__, url_prefix='/api/gesture')

@bp.route('/', methods=['POST'])
def perform_action():
    data = request.json  # Expecting JSON input with a 'gesture' field, e.g., {"gesture": "peace_sign"}
    if not data or "gesture" not in data:
        current_app.logger.error("Error: No gesture provided")
        return jsonify({"status": "error", "message": "No gesture provided"}), 400

    gesture = data['gesture']
    current_app.logger.info(f"Received gesture: {gesture}")  # Log gesture in backend log

    # Update the latest gesture in the backend
    try:
        update_url = url_for('update_gesture', _external=True)
        requests.post(update_url, json={"gesture": gesture}, timeout=3)
    except Exception as e:
        current_app.logger.error(f"Error updating latest gesture: {e}")

    gesture_actions = {
        "peace_sign": {"action": "open_url", "data": "https://www.google.com"},
        "thumbs_up": {"action": "notify", "data": "thumbs up!"},
        "index_up": {"action": "notify", "data": "index finger up!"},
        "rock_and_roll_salute": {"action": "notify", "data": "rock and roll!"},
        "fist": {"action": "notify", "data": "fists up!"},
        "l_sign": {"action": "notify", "data": "L Sign!"}
    }

    action = gesture_actions.get(gesture, {"action": "none", "data": "No action available"})
    current_app.logger.info(f"Action to perform: {action}")  # Log action being performed

    return jsonify({"status": "success", "action": action})
