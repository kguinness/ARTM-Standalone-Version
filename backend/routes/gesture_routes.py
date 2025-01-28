from flask import Blueprint, request, jsonify
import requests

bp = Blueprint('gestures', __name__, url_prefix='/api/gesture')


@bp.route('/', methods=['POST'])
def perform_action():
    data = request.json  # Expecting JSON input with a 'gesture' field, i.e. {"gesture" : "peace_sign"}
    if not data or "gesture" not in data:
        print("Error: No gesture provided")
        return jsonify({"status": "error", "message": "No gesture provided"}), 400


    gesture = data['gesture']
    print(f"Recieved gesture: {gesture}") #log gesture in backend (command prompt)

    try:
        requests.post("http://127.0.0.1:5000/update_gesture", json={"gesture": gesture}) #updates backend log
    except Exception as e:
        print(f"Error updating latest gesture: {e}")

    gesture_actions = {
        "peace_sign": {"action": "open_url", "data": "https://www.google.com"},
        "thumbs_up": {"action": "notify", "data": "thumbs up!"},
        "index_up": {"action": "notify", "data": "index finger up!"},
        "rock_and_roll_salute": {"action": "notify", "data": "rock and roll!"},
        "fist": {"action": "notify", "data": "fists up!"},
        "l_sign": {"action": "notify", "data": "L Sign!"}

    }

    action = gesture_actions.get(gesture, {"action": "none", "data": "No action available"})
    print(f"Action to perform: {action}") #Logs action being performed in backend (command prompt)

    return jsonify({"status": "success", "action": action})
