from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import mediapipe as mp
from utils.gesture_utils import detect_peace_sign, detect_thumbs_up


class GestureCapturePage(QWidget):
    def __init__(self, parent=None):
        super(GestureCapturePage, self).__init__(parent)
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands_detector = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5
        )
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_label)

        self.result_label = QLabel("No hand detected", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        self.custom_capture_button = QPushButton("Capture Gesture", self)
        self.custom_capture_button.setObjectName("CaptureGestureButton")
        self.custom_capture_button.clicked.connect(self.capture_custom_gesture)
        layout.addWidget(self.custom_capture_button, alignment=Qt.AlignCenter)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands_detector.process(frame_rgb)
        detected_gesture = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                if detect_peace_sign(hand_landmarks):
                    detected_gesture = "Peace Sign Detected"
                    break
                elif detect_thumbs_up(hand_landmarks):
                    detected_gesture = "Thumbs Up Detected"
                    break
            if detected_gesture:
                self.result_label.setText(detected_gesture)
            else:
                self.result_label.setText("No recognized gesture")
        else:
            self.result_label.setText("No hand detected")

        frame_rgb_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb_display.shape
        bytes_per_line = ch * w
        qt_img = QImage(frame_rgb_display.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

    def capture_custom_gesture(self):
        current_text = self.result_label.text()
        self.result_label.setText(f"Captured Gesture: {current_text}")

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap.isOpened():
            self.cap.release()
        self.hands_detector.close()
        super().closeEvent(event)
