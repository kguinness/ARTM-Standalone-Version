import json
import os
from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

PROFILE_FILE = "profiles.json"

class ProfileSelectionPage(QWidget):
    # Signal to notify that a profile was selected.
    profileSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ProfileSelectionPage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Create a vertical layout for the page.
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        # Title label.
        title = QLabel("Select a Profile")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.layout.addWidget(title)

        # Load existing profiles and create buttons.
        self.profile_buttons = []
        self.load_profiles()

        # "Add Profile" button.
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
        # Emit the signal so that the main window can handle the selection.
        print("Selecting profile:", profile)
        self.profileSelected.emit(profile)

    def get_profiles(self):
        if os.path.exists(PROFILE_FILE):
            try:
                with open(PROFILE_FILE, "r") as file:
                    profiles = json.load(file)
                    if isinstance(profiles, list):
                        return profiles
                    else:
                        return []
            except Exception as e:
                print("Error loading profiles:", e)
                return []
        return []

    def clear_profile_buttons(self):
        for btn in self.profile_buttons:
            self.layout.removeWidget(btn)
            btn.deleteLater()
        self.profile_buttons.clear()

    def open_profile_creation(self):
        # Use self.window() to get the top-level window
        main_window = self.window()
        if hasattr(main_window, "setCurrentPage"):
            main_window.setCurrentPage("profile_creation")
        else:
            print("Main window does not have setCurrentPage method.")
