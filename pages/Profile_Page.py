import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class ProfilePage(QWidget):
    def __init__(self):
        super().__init__()

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Labels and input fields
        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        self.layout.addWidget(self.label_username)
        self.layout.addWidget(self.input_username)

        self.label_email = QLabel("Email:")
        self.input_email = QLineEdit()
        self.layout.addWidget(self.label_email)
        self.layout.addWidget(self.input_email)

        # Buttons
        self.update_button = QPushButton("Update Profile")
        self.update_button.clicked.connect(self.update_profile)
        self.layout.addWidget(self.update_button)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)

        self.user_id = None  # Store the logged-in user ID

    def load_profile(self, user_id):
        """Load the user profile from the backend."""
        self.user_id = user_id
        try:
            response = requests.get(f"http://127.0.0.1:5000/users/profile/{user_id}")
            if response.status_code == 200:
                user_data = response.json()
                self.input_username.setText(user_data["username"])
                self.input_email.setText(user_data["email"])
            else:
                QMessageBox.warning(self, "Error", "Failed to load profile")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not connect to server: {e}")

    def update_profile(self):
        """Update the user's profile in the backend."""
        if not self.user_id:
            QMessageBox.warning(self, "Error", "No user is logged in.")
            return

        updated_data = {
            "username": self.input_username.text(),
            "email": self.input_email.text()
        }

        try:
            response = requests.put(f"http://127.0.0.1:5000/users/profile/{self.user_id}", json=updated_data)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Profile updated successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to update profile")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not connect to server: {e}")

    def logout(self):
        """Log out the user."""
        self.user_id = None
        self.input_username.clear()
        self.input_email.clear()
        QMessageBox.information(self, "Logout", "You have been logged out.")
