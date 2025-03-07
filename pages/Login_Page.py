from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal  # Import pyqtSignal

class LoginPage(QWidget):
    login_success = pyqtSignal(int)  # 🔹 Signal emits user ID when login is successful

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Login Page")
        self.layout.addWidget(self.label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.attempt_login)
        self.layout.addWidget(self.login_button)

    def attempt_login(self):
        import requests
        email = self.email_input.text()
        password = self.password_input.text()

        response = requests.post("http://127.0.0.1:5000/users/login", json={"email": email, "password": password})

        if response.status_code == 200:
            user_id = response.json().get("user_id")
            print(f"Login successful, user ID: {user_id}")  # Debug print
            self.login_success.emit(user_id)  # 🔹 Emit the signal on success
            QMessageBox.information(self, "Success", "Login successful!")
        else:
            QMessageBox.warning(self, "Error", "Invalid email or password")
