from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import mediapipe as mp
from utils.gesture_utils import (
    detect_peace_sign,
    detect_thumbs_up,
    detect_index_up,
    detect_fist,
    detect_letter_l,
)


class GestureCapturePage(QWidget):
    def __init__(self, parent=None):
        super(GestureCapturePage, self).__init__(parent)

        # 1) Make the page background black to match your screenshot's style.
        self.setStyleSheet("background-color: #000000;")

        # 2) Open the default camera (index 0). Adjust if needed (e.g., use 1).
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open video capture.")
        else:
            print("Camera successfully opened.")

        # 3) Initialize MediaPipe Hands and drawing utilities.
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands_detector = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5
        )

        # 4) Set up a QTimer to call update_frame() ~every 30 ms (33 FPS).
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # 5) Build the UI layout.
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        # (A) Video feed label
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        # Minimum size ensures there's space for the feed.
        self.video_label.setMinimumSize(640, 480)
        layout.addWidget(self.video_label)

        # (B) Result label (displays detected gesture)
        self.result_label = QLabel("No hand detected", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: #FFFFFF; font-size: 16px;")
        layout.addWidget(self.result_label)

        # (C) "Capture Gesture" button at the bottom
        self.capture_button = QPushButton("Capture Gesture", self)
        self.capture_button.setStyleSheet(
            "QPushButton { background-color: #FF69B4; color: #000; font-weight: bold; }"
        )
        self.capture_button.clicked.connect(self.capture_custom_gesture)
        layout.addWidget(self.capture_button, alignment=Qt.AlignCenter)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Warning: No frame captured from camera.")
            return

        # Convert the captured frame from BGR (OpenCV default) to RGB.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame using MediaPipe Hands
        results = self.hands_detector.process(frame_rgb)
        detected_gesture = ""

        # If hands are detected, check for gestures & draw landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw the hand landmarks on the RGB frame
                self.mp_drawing.draw_landmarks(
                    frame_rgb,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                # Check multiple gestures in order
                if detect_peace_sign(hand_landmarks):
                    detected_gesture = "Peace Sign Detected"
                    break
                elif detect_thumbs_up(hand_landmarks):
                    detected_gesture = "Thumbs Up Detected"
                    break
                elif detect_index_up(hand_landmarks):
                    detected_gesture = "Index Up Detected"
                    break
                elif detect_fist(hand_landmarks):
                    detected_gesture = "Fist Detected"
                    break
                elif detect_letter_l(hand_landmarks):
                    detected_gesture = "Letter L Detected"
                    break

            # If none matched, set to "No recognized gesture"
            if not detected_gesture:
                detected_gesture = "No recognized gesture"
        else:
            detected_gesture = "No hand detected"

        # Update the result label text
        self.result_label.setText(detected_gesture)

        # Convert the processed RGB frame to QImage for display
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Display the QImage in the video_label
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

    def capture_custom_gesture(self):
        current_text = self.result_label.text()
        self.result_label.setText("Captured Gesture: " + current_text)

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap.isOpened():
            self.cap.release()
        self.hands_detector.close()
        super().closeEvent(event)

    def load_styles(self):
        try:
            with open("src/pages/gesture_capture/gesture_capture_page.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Error loading gesture_capture_page.qss:", e)
