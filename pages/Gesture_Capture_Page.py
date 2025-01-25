import cv2
import sys
import time
import numpy as np
import mediapipe as mp
import requests
import webbrowser

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

from gesture_utils import (
    detect_peace_sign,
    detect_thumbs_up,
    detect_index_upwards,
    detect_rock_and_roll_salute,
    detect_fist,
    detect_letter_l
)

class GestureCapturePage(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the page layout
        self.layout = QVBoxLayout()
        #self.layout.addWidget(self.video_label)
        #self.video_label("Gesture detection in progress...")
        self.setLayout(self.layout)
        self.google_opened = False  # Flag to track if Google has been opened


        # Qlabel for gesture detection status
        self.status_label = QLabel("Gesture detection in progress...")
        self.layout.addWidget(self.status_label)


        # Create a label to display the video feed
        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)


        # Initialize video capture
        self.cap = cv2.VideoCapture(0)

        # Set up a QTimer to update the video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Initialize MediaPipe Hands class
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

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

        self.GESTURE_DETECTION_TIME = 1.0  # 1 second

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

        # Convert the image from BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for hand tracking
        hand_results = self.hands.process(rgb_frame)

        # Initialize gesture variable
        gesture = 'No gesture detected'

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

                if detect_peace_sign(hand_landmarks):
                    gesture = 'Peace Sign Detected'
                    if self.gesture_timers['Peace Sign'] == 0:
                        self.gesture_timers['Peace Sign'] = time.time()
                    #elif time.time() - self.gesture_timers['Peace Sign'] >= self.GESTURE_DETECTION_TIME:
                    elif time.time() - self.gesture_timers['Peace Sign'] >= 3: #3 seconds
                        gesture = 'Peace Sign Detected'
                        if not self.google_opened:  # Only open Google once
                            webbrowser.open("https://www.google.com")
                            self.google_opened = True  # Set the flag to prevent reopening
                else:
                    self.gesture_timers['Peace Sign'] = 0
                    self.google_opened = False  # Reset the flag if gesture is no longer detected




                if detect_thumbs_up(hand_landmarks):
                    gesture = 'Thumbs Up Detected'
                    if self.gesture_timers['Thumbs Up'] == 0:
                        self.gesture_timers['Thumbs Up'] = time.time()
                    elif time.time() - self.gesture_timers['Thumbs Up'] >= 3:
                        gesture = 'Thumbs Up Detected'
                else:
                    self.gesture_timers['Thumbs Up'] = 0

                if detect_index_upwards(hand_landmarks):
                    gesture = 'Index Up Detected'
                    if self.gesture_timers['Index Up'] == 0:
                        self.gesture_timers['Index Up'] = time.time()
                    elif time.time() - self.gesture_timers['Index Up'] >= 3:
                        gesture = 'Index Up Detected'
                else:
                    self.gesture_timers['Index Up'] = 0

                if detect_rock_and_roll_salute(hand_landmarks):
                    gesture = 'Rock and Roll Salute Detected'
                    if self.gesture_timers['Rock and Roll Salute'] == 0:
                        self.gesture_timers['Rock and Roll Salute'] = time.time()
                    elif time.time() - self.gesture_timers['Rock and Roll Salute'] >= 3:
                        gesture = 'Rock and Roll Salute Detected'
                else:
                    self.gesture_timers['Rock and Roll Salute'] = 0

                if detect_fist(hand_landmarks):
                    gesture = 'Fist Gesture Detected'
                    if self.gesture_timers['Fist'] == 0:
                        self.gesture_timers['Fist'] = time.time()
                    elif time.time() - self.gesture_timers['Fist'] >= 3:
                        gesture = 'Fist Gesture Detected'
                else:
                    self.gesture_timers['Fist'] = 0

                if detect_letter_l(hand_landmarks):
                    gesture = 'L Sign Detected'
                    if self.gesture_timers['L Sign'] == 0:
                        self.gesture_timers['L Sign'] = time.time()
                    elif time.time() - self.gesture_timers['L Sign'] >= 3:
                        gesture = 'L Sign Detected'
                else:
                    self.gesture_timers['L Sign'] = 0


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

        # Update the status lebel with the detected gesture
        if gesture != 'No gesture detected':
            self.status_label.setText(f"Detected Gesture: {gesture}")
        else:
            self.status_label.setText("Gesture detection in progress...")




    def closeEvent(self, event):
        # Release the video capture when closing the page
        self.cap.release()
        self.timer.stop()
        super().closeEvent(event)

