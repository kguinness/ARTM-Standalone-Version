from flask import Flask, render_template, request, Response
import cv2
import numpy as np
import mediapipe as mp
import time

app = Flask(__name__)

# Dictionary to keep track of gesture timestamps
gesture_timers = {
    'Peace Sign': 0,
    'Thumbs Up': 0,
    'Index Up': 0,
    'Rock and Roll Salute': 0
}

# Constant for the required time for detecting the gesture
GESTURE_DETECTION_TIME = 3  # 3 seconds

# Initialize MediaPipe Pose and Hands classes
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose()
hands = mp_hands.Hands()

# Initialize MediaPipe drawing utils
mp_drawing = mp.solutions.drawing_utils


# Function to detect peace sign gesture
def detect_peace_sign(hand_landmarks):
    # Define the index, middle, ring, and pinky finger tip landmarks
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # Check if the index and middle fingers are extended and the others are curled
    index_extended = index_finger_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_extended = middle_finger_tip.y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_curled = ring_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_curled = pinky_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

    if index_extended and middle_extended and ring_curled and pinky_curled:
        return True
    return False


def detect_thumbs_up(hand_landmarks):
    # Define the landmarks for the thumb and other fingers
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # Check if the thumb is extended (thumb tip above thumb IP joint)
    thumb_extended = thumb_tip.y < thumb_ip.y

    # Check if all other fingers are curled
    index_curled = index_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_curled = middle_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_curled = ring_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_curled = pinky_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

    # If thumb is extended and all other fingers are curled, it's a thumbs up
    if thumb_extended and index_curled and middle_curled and ring_curled and pinky_curled:
        return True
    return False


def detect_index_upwards(hand_landmarks):
    # Get landmarks for index, middle, ring, and pinky fingers
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # Check if the index finger is extended (tip above its PIP joint)
    index_extended = index_finger_tip.y < index_finger_pip.y

    # Check if the other fingers are curled (tips below their PIP joints)
    middle_curled = middle_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_curled = ring_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_curled = pinky_finger_tip.y > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

    # Return True if only the index finger is extended upwards
    if index_extended and middle_curled and ring_curled and pinky_curled:
        return True
    return False

# Function to detect rock and roll salute gesture
def detect_rock_and_roll_salute(hand_landmarks):
    # Define the landmarks for each finger
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]

    pinky_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    # Check if the thumb, index, and pinky are extended
    thumb_extended = thumb_tip.y < thumb_ip.y
    index_extended = index_finger_tip.y < index_finger_pip.y
    pinky_extended = pinky_finger_tip.y < pinky_finger_pip.y

    # Check if the middle and ring fingers are curled
    middle_curled = middle_finger_tip.y > middle_finger_pip.y
    ring_curled = ring_finger_tip.y > ring_finger_pip.y

    # If the conditions for the rock and roll salute are met, return True
    if thumb_extended and index_extended and pinky_extended and middle_curled and ring_curled:
        return True
    return False




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed', methods=['POST'])
def video_feed():
    # Receive the image from the client
    nparr = np.frombuffer(request.data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Flip the frame horizontally for a selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the image from BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for pose estimation and hand tracking
    pose_results = pose.process(rgb_frame)
    hand_results = hands.process(rgb_frame)

    # Initialize gesture variable
    gesture = 'No gesture detected'

    # Draw the pose landmarks on the original frame
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            pose_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
        )

        # Bottom-right box holding gesture symbol
        box_x, box_y = frame.shape[1] - 150, frame.shape[0] - 50
        box_w, box_h = 140, 40
        gesture_detected = False  # Flag to check if any gesture is detected

    # Draw hand landmarks and detect gestures
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            # Draw the hand landmarks on the frame
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
            )

            # Get bounding box coordinates for the hand
            x_min = min([landmark.x for landmark in hand_landmarks.landmark])
            y_min = min([landmark.y for landmark in hand_landmarks.landmark])
            x_max = max([landmark.x for landmark in hand_landmarks.landmark])
            y_max = max([landmark.y for landmark in hand_landmarks.landmark])

            # Convert normalized coordinates to image coordinates
            h, w, _ = frame.shape
            x_min = int(x_min * w)
            y_min = int(y_min * h)
            x_max = int(x_max * w)
            y_max = int(y_max * h)

            # Draw a blue rectangle around the hand
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

            # Check for the Peace Sign gesture
            if detect_peace_sign(hand_landmarks):
                if gesture_timers['Peace Sign'] == 0:
                    # Start the timer when the gesture is first detected
                    gesture_timers['Peace Sign'] = time.time()
                elif time.time() - gesture_timers['Peace Sign'] >= GESTURE_DETECTION_TIME:
                    # If 3 seconds have passed, confirm the gesture
                    gesture = 'Peace Sign Detected'
                    gesture_detected = True
                    cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                # Reset the timer if the gesture is not detected
                gesture_timers['Peace Sign'] = 0

            # Check for the Thumbs Up gesture
            if detect_thumbs_up(hand_landmarks):
                if gesture_timers['Thumbs Up'] == 0:
                    gesture_timers['Thumbs Up'] = time.time()
                elif time.time() - gesture_timers['Thumbs Up'] >= GESTURE_DETECTION_TIME:
                    gesture = 'Thumbs Up Detected'
                    gesture_detected = True
                    cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                gesture_timers['Thumbs Up'] = 0

            # Check for the Index Up gesture
            if detect_index_upwards(hand_landmarks):
                if gesture_timers['Index Up'] == 0:
                    gesture_timers['Index Up'] = time.time()
                elif time.time() - gesture_timers['Index Up'] >= GESTURE_DETECTION_TIME:
                    gesture = 'Index Up Detected'
                    gesture_detected = True
                    cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                gesture_timers['Index Up'] = 0

            # Check for the Rock and Roll Salute gesture
            if detect_rock_and_roll_salute(hand_landmarks):
                if gesture_timers['Rock and Roll Salute'] == 0:
                    gesture_timers['Rock and Roll Salute'] = time.time()
                elif time.time() - gesture_timers['Rock and Roll Salute'] >= GESTURE_DETECTION_TIME:
                    gesture = 'Rock and Roll Salute Detected'
                    gesture_detected = True
                    cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                gesture_timers['Rock and Roll Salute'] = 0

        # Draw the box at the bottom right if a gesture is detected
        if gesture_detected:
            # Draw the box
            box_x = frame.shape[1] - 60  # Move closer to the right edge
            box_y = frame.shape[0] - 70  # Move slightly up from the bottom

            box_size = 50
            cv2.rectangle(frame, (box_x, box_y), (box_x + box_size, box_y + box_size), (0, 255, 0), 2)

    # Encode the frame back to JPEG to send back to the client
    ret, jpeg = cv2.imencode('.jpg', frame)
    frame_encoded = jpeg.tobytes()

    # Send the gesture as a response header
    response = Response(frame_encoded, mimetype='image/jpeg')
    response.headers['Gesture'] = gesture

    return response


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

