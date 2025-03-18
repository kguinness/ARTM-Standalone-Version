import json
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt

PROFILE_FILE = "profiles.json"

class ProfileCreationPage(QWidget):
    def __init__(self, parent=None):
        super(ProfileCreationPage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        title = QLabel("Create a New Profile")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.layout.addWidget(title)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter profile name")
        self.layout.addWidget(self.name_input)

        create_button = QPushButton("Create Profile")
        create_button.setObjectName("CreateProfileButton")
        create_button.clicked.connect(self.create_profile)
        self.layout.addWidget(create_button)

        back_button = QPushButton("Back")
        back_button.setObjectName("BackButton")
        back_button.clicked.connect(lambda: self.window().setCurrentPage("profile_selection"))
        self.layout.addWidget(back_button)

    def create_profile(self):
        profile_name = self.name_input.text().strip()
        if not profile_name:
            return
        profiles = self.get_profiles()
        if profile_name in profiles:
            print("Profile name already exists!")
            return
        profiles.append(profile_name)
        self.save_profiles(profiles)
        self.window().setCurrentPage("profile_selection")

    def get_profiles(self):
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE, "r") as file:
                return json.load(file)
        return []

    def save_profiles(self, profiles):
        with open(PROFILE_FILE, "w") as file:
            json.dump(profiles, file)
