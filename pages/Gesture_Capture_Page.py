import cv2
import sys
import time
import numpy as np
import mediapipe as mp
import requests
import webbrowser

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

from gesture_utils import (
    detect_peace_sign,
    detect_thumbs_up,
    detect_index_up,
    detect_rock_and_roll_salute,
    detect_fist,
    detect_letter_l
)

class GestureCapturePage(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the page layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.google_opened = False  # Flag to track if Google has been opened

        # Create and configure the QLabel for video feed
        self.video_label = QLabel()
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setScaledContents(True)  # Enable dynamic resizing
        self.layout.addWidget(self.video_label)

        # QLabel for gesture detection status
        self.status_label = QLabel("Gesture detection in progress...")
        self.layout.addWidget(self.status_label)

        self.countdown_label = QLabel("")
        self.layout.addWidget(self.countdown_label)

        # Initialize video capture
        self.cap = cv2.VideoCapture(0)

        # Set up a QTimer to update the video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Check if 30ms is too frequent

        # Initialize MediaPipe Hands class
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,  # Detect only one hand
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Initialize MediaPipe drawing utils
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize gesture timers
        self.gesture_timers = {
            'Peace Sign': 0,
            'Thumbs Up': 0,
            'Index Up': 0,
            'Rock and Roll Salute': 0,
            'Fist': 0,
            'L Sign': 0
        }

        self.gesture_flags = {
            'Peace Sign': False,
            'Thumbs Up': False,
            'Index Up': False,
            'Rock and Roll Salute': False,
            'Fist': False,
            'L Sign': False
        }

        self.gesture_map = {
            "Peace Sign": detect_peace_sign,
            "Thumbs Up": detect_thumbs_up,
            "Index Up": detect_index_up,
            "Rock and Roll Salute": detect_rock_and_roll_salute,
            "Fist": detect_fist,
            "L Sign": detect_letter_l,
        }

        self.GESTURE_DETECTION_TIME = 1.0  # 1 second


    # command to send detected gesture to flask backend
    def send_gesture_to_backend(self, gesture):

        try:
            response = requests.post(
                "http://127.0.0.1:5000/api/gesture/",
                json={"gesture": gesture}
            )
            if response.status_code == 200:
                action = response.json().get("action", {})
                self.perform_action(action)
            else:
                print("Error from backend:", response.json().get("message"))
        except Exception as e:
            print("Error communicating with backend:", e)

    # command to perform the action returned by the backend
    def perform_action(self, action):
        if action["action"] == "open_url":
            webbrowser.open(action["data"])  # open the url in default browser
        elif action["action"] == "notify":
            print(action["data"])  # display notification
        else:
            print("No valid action for the gesture")


    # Insert Gesture Box in Bottom Right Corner
    def draw_box_on_frame(self, frame):
        # Get frame dimensions
        height, width, _ = frame.shape

        # Define box size and position (bottom-right corner)
        box_width, box_height = 100, 100  # Adjust box size as needed
        top_left_x = width - box_width - 10  # 10px margin from the right edge
        top_left_y = height - box_height - 10  # 10px margin from the bottom edge
        bottom_right_x = width - 10
        bottom_right_y = height - 10

        # Draw the rectangle
        cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (250, 0, 0), 2)

    def update_frame(self):
        # Read a frame from the webcam
        ret, frame = self.cap.read()
        if not ret:
            return

        # Flip the frame horizontally for a selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the frame from BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to QImage
        height, width, channel = rgb_frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Resize the QPixmap to fit the QLabel while maintaining aspect ratio
        pixmap = QPixmap.fromImage(q_img).scaled(
            self.video_label.size(),  # Use QLabel's current size
            Qt.KeepAspectRatio,  # Maintain aspect ratio
            Qt.SmoothTransformation  # Smooth scaling for better quality
        )

        # Set the QLabel pixmap
        self.video_label.setPixmap(pixmap)

        # Process the frame for hand tracking
        hand_results = self.hands.process(rgb_frame)

        # Initialize gesture variable
        gesture = 'No gesture detected'
        countdown_time = ""

        # Draw hand landmarks and detect gestures
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Draw the hand landmarks on the frame
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                )

                # Check for gestures
                for gesture_name, detect_function in self.gesture_map.items():
                    if detect_function(hand_landmarks):
                        gesture = gesture_name
                        if self.gesture_timers[gesture_name] == 0:
                            # Start gesture timer
                            self.gesture_timers[gesture_name] = time.time()
                        elif (
                            time.time() - self.gesture_timers[gesture_name] >= 3
                            and not self.gesture_flags[gesture_name]
                        ):
                            self.send_gesture_to_backend(gesture_name.lower().replace(" ", "_"))
                            self.gesture_flags[gesture_name] = True
                        else:
                            elapsed_time = time.time() - self.gesture_timers[gesture_name]
                            countdown_time = f"Action in: {3 - int(elapsed_time)}s"
                    else:
                        self.gesture_timers[gesture_name] = 0
                        self.gesture_flags[gesture_name] = False


        # Draw the gesture box in the bottom-right corner
        self.draw_box_on_frame(frame)

        # Display the gesture on the frame
        #cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Convert the frame back to QImage to display in QLabel
        height, width, channel = frame.shape
        bytes_per_line = 3 * width

        # Convert the frame from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to QImage
        q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)


        # Set the pixmap of the video_label to the new frame
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

        if countdown_time:
            self.countdown_label.setText(countdown_time)
        else:
            self.countdown_label.setText("")

        # Update the status lebel with the detected gesture
        if gesture != 'No gesture detected':
            self.status_label.setText(f"Detected Gesture: {gesture}")
        else:
            self.status_label.setText("Gesture detection in progress...")

    def resizeEvent(self, event):
        """Handle window resizing and update the video feed."""
        self.update_frame()  # Force a frame update when the window is resized
        super().resizeEvent(event)

    def closeEvent(self, event):
        # Release the video capture when closing the page
        self.cap.release()
        self.timer.stop()
        super().closeEvent(event)

