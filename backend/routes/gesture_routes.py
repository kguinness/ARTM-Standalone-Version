'''
from flask import Blueprint, request, jsonify

bp = Blueprint('gestures', __name__, url_prefix='/api/gestures')

# Define gesture-action mappings
gesture_actions = {
    "peace_sign": {"action": "open_url", "data": "https://www.google.com"}
    #"thumbs_up": {"action": "notify", "data": "You performed a thumbs up!"},
    #"rock_and_roll": {"action": "play_sound", "data": "sound.wav"},
}

@bp.route('/perform', methods=['POST'])
def perform_gesture_action():
    data = request.json  # Expecting JSON input with a 'gesture' field
    gesture = data.get('gesture')

    if gesture in gesture_actions:
        action = gesture_actions[gesture]
        return jsonify({"status": "success", "action": action}), 200
    else:
        return jsonify({"status": "error", "message": "Gesture not recognized"}), 400
'''