from flask import Flask, request, jsonify
from routes.gesture_routes import bp as gesture_bp

app = Flask(__name__)

# register gesture routes
app.register_blueprint(gesture_bp)

#store the latest recognized gesture to display in backend log
app.config["LATEST_GESTURE"] = "No gestures detected yet."



@app.route('/update_gesture', methods=['POST'])
def update_gesture():
    global latest_gesture
    data = request.json
    if "gesture" in data:
        app.config["LATEST_GESTURE"] = data["gesture"] # update stored gesture
        return jsonify({"status": "success", "message": "Latest gesture updated."})
    return jsonify({"status": "error", "message": "No gesture provided."}), 400

@app.route('/')
def home():
    return jsonify({
        "message": "Flask backend is running!",
        "latest_gesture": app.config["LATEST_GESTURE"],
        "most_latest_gesture": "test"
    })

if __name__ == "__main__":
    app.run(debug=True)