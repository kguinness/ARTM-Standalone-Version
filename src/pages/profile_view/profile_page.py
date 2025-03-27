from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class ProfilePage(QWidget):
    def __init__(self, parent=None):
        super(ProfilePage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.profile_label = QLabel("Profile Information")
        self.profile_label.setObjectName("ProfileLabel")
        self.profile_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.profile_label)

    def load_profile(self, profile_name):
        self.profile_label.setText(f"Logged in as: {profile_name}")

    def load_styles(self):
        try:
            with open("src/pages/profile_view/profile_page.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Error loading profile_page.qss:", e)
