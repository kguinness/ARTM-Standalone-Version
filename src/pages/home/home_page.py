import json
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

PROFILE_FILE = "profiles.json"

class ProfileCreationPage(QWidget):
    profileCreated = pyqtSignal()
    backRequested = pyqtSignal()

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
        back_button.clicked.connect(self.go_back)
        self.layout.addWidget(back_button)

    def create_profile(self):
        profile_name = self.name_input.text().strip()
        if not profile_name:
            QMessageBox.warning(self, "Input Error", "Profile name cannot be empty.")
            return
        profiles = self.get_profiles()
        if profile_name in profiles:
            QMessageBox.warning(self, "Duplicate Profile", "Profile name already exists!")
            return
        profiles.append(profile_name)
        if self.save_profiles(profiles):
            print(f"Profile '{profile_name}' created successfully.")
            self.profileCreated.emit()
        else:
            print("Failed to save profile.")

    def go_back(self):
        self.backRequested.emit()

    def get_profiles(self):
        if os.path.exists(PROFILE_FILE):
            try:
                with open(PROFILE_FILE, "r") as file:
                    content = file.read().strip()
                    if not content:
                        return []
                    profiles = json.loads(content)
                    if isinstance(profiles, list):
                        return profiles
                    else:
                        print("Profiles file is not a list. Using empty list instead.")
                        return []
            except Exception as e:
                print("Error reading profiles:", e)
                return []
        return []

    def save_profiles(self, profiles):
        try:
            with open(PROFILE_FILE, "w") as file:
                json.dump(profiles, file)
            return True
        except Exception as e:
            print("Error saving profiles:", e)
            return False

    def load_home_page_styles(self):
        try:
            with open("src/pages/home/home_page.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Error loading home_page.qss:", e)
