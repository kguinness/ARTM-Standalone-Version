from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class ProfilePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # A label to display user info
        self.profile_label = QLabel("Profile Page")
        self.profile_label.setObjectName("ProfileLabel")
        layout.addWidget(self.profile_label, alignment=Qt.AlignCenter)

        # Placeholder for additional profile info
        details_label = QLabel("Your profile details go here.")
        details_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(details_label, alignment=Qt.AlignCenter)

    def load_profile(self, user_id, username):
        """ Called by ARTM.py after login to pass user info. """
        self.profile_label.setText(f"Logged in as: {username}")
