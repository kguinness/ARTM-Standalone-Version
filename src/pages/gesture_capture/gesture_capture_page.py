from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import mediapipe as mp
from utils.gesture_utils import detect_peace_sign, detect_thumbs_up


class GestureCapturePage(QWidget):
    def __init__(self, parent=None):
        super(GestureCapturePage, self).__init__(parent)
        # Open the default camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open video capture.")
        else:
            print("Camera successfully opened.")

        # Initialize MediaPipe Hands and drawing utilities.
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands_detector = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5
        )

        # Set up a timer to update the video feed (approximately 33 FPS).
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Video feed label with a minimum size.
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(640, 480)
        layout.addWidget(self.video_label)

        # Label to display detected gesture.
        self.result_label = QLabel("No hand detected", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        # "Capture Gesture" button (optional; for custom capture).
        self.capture_button = QPushButton("Capture Gesture", self)
        self.capture_button.clicked.connect(self.capture_custom_gesture)
        layout.addWidget(self.capture_button, alignment=Qt.AlignCenter)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Warning: No frame captured.")
            return

        # Convert the frame from BGR to RGB.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands.
        results = self.hands_detector.process(frame_rgb)
        detected_gesture = "No hand detected"
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on the RGB frame.
                self.mp_drawing.draw_landmarks(frame_rgb, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                # Check for gestures.
                if detect_peace_sign(hand_landmarks):
                    detected_gesture = "Peace Sign Detected"
                    break
                elif detect_thumbs_up(hand_landmarks):
                    detected_gesture = "Thumbs Up Detected"
                    break
            if detected_gesture == "":
                detected_gesture = "No recognized gesture"
        self.result_label.setText(detected_gesture)

        # Convert processed frame to QImage and display it.
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(image))

    def capture_custom_gesture(self):
        current_text = self.result_label.text()
        self.result_label.setText(f"Captured Gesture: {current_text}")

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap.isOpened():
            self.cap.release()
        self.hands_detector.close()
        super().closeEvent(event)
