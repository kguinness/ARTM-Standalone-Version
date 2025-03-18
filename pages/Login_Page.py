from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal, Qt

class LoginPage(QWidget):
    # Signals
    login_success = pyqtSignal(int)
    register_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main vertical layout, centered
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Large "Log in" title
        title_label = QLabel("Log in")
        title_label.setObjectName("LoginTitle")  # For stylesheet
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedWidth(300)
        self.email_input.setObjectName("LoginField")
        layout.addWidget(self.email_input, alignment=Qt.AlignCenter)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        self.password_input.setObjectName("LoginField")
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        # "Log in" button
        self.login_button = QPushButton("Log in")
        self.login_button.setObjectName("LoginButton")
        self.login_button.clicked.connect(self.attempt_login)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        layout.addSpacing(10)

        # "or, sign up"
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignCenter)

        or_label = QLabel("or,")
        or_label.setObjectName("OrLabel")
        bottom_layout.addWidget(or_label)

        signup_link = QPushButton("sign up")
        signup_link.setObjectName("SignupLink")
        signup_link.setFlat(True)
        signup_link.clicked.connect(self.handle_register)
        bottom_layout.addWidget(signup_link)

        layout.addLayout(bottom_layout)

    def attempt_login(self):
        import requests
        email = self.email_input.text()
        password = self.password_input.text()

        response = requests.post(
            "http://127.0.0.1:5000/users/login",
            json={"email": email, "password": password}
        )

        if response.status_code == 200:
            user_id = response.json().get("user_id")
            print(f"Login successful, user ID: {user_id}")
            self.login_success.emit(user_id)
            QMessageBox.information(self, "Success", "Login successful!")
        else:
            QMessageBox.warning(self, "Error", "Invalid email or password")

    def handle_register(self):
        self.register_requested.emit()
