import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox

class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Create New Account")
        self.layout.addWidget(self.label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.layout.addWidget(self.username_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)
        self.layout.addWidget(self.register_button)

    #Send user registration data to the backend
    def register_user(self):

        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        data = {"username": username, "email": email, "password": password}
        response = requests.post("http://127.0.0.1:5000/users/register", json=data)

        if response.status_code == 201:
            QMessageBox.information(self, "Success", "User registered successfully!")
        elif response.status_code == 400:
            QMessageBox.warning(self, "Error", "Username or email already exists.")
        else:
            QMessageBox.warning(self, "Error", "Failed to register user.")
