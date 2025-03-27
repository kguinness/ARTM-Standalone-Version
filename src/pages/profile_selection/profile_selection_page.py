import json
import os
from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

PROFILE_FILE = "profiles.json"


class ProfileSelectionPage(QWidget):
    profileSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ProfileSelectionPage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        title = QLabel("Select a Profile")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.layout.addWidget(title)

        self.profile_buttons = []
        self.load_profiles()

        add_profile_btn = QPushButton("Add Profile")
        add_profile_btn.setObjectName("AddProfileButton")
        add_profile_btn.clicked.connect(self.open_profile_creation)
        self.layout.addWidget(add_profile_btn)

    def load_profiles(self):
        self.clear_profile_buttons()
        profiles = self.get_profiles()
        for profile in profiles:
            btn = QPushButton(profile)
            btn.setObjectName("ProfileButton")
            btn.clicked.connect(partial(self.select_profile, profile))
            self.layout.addWidget(btn)
            self.profile_buttons.append(btn)

    def select_profile(self, profile):
        print("Selecting profile:", profile)
        self.profileSelected.emit(profile)

    def get_profiles(self):
        if os.path.exists(PROFILE_FILE):
            try:
                with open(PROFILE_FILE, "r") as file:
                    profiles = json.load(file)
                    if isinstance(profiles, list):
                        return profiles
            except Exception as e:
                print("Error loading profiles:", e)
        return []

    def clear_profile_buttons(self):
        for btn in self.profile_buttons:
            self.layout.removeWidget(btn)
            btn.deleteLater()
        self.profile_buttons.clear()

    def open_profile_creation(self):
        # Assuming the parent of this page is the QStackedWidget that holds both
        # the profile selection (index 0) and profile creation page (index 1).
        if self.parent() is not None:
            print("Switching to Profile Creation page.")
            self.parent().setCurrentIndex(1)
        else:
            print("No parent found for profile selection page.")

    def load_styles(self):
        try:
            with open("src\pages\profile_selection\profile_selection_page.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Error loading profile_selection_page.qss:", e)
