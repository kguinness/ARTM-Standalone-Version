from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal


class ProfileCreationPage(QWidget):
    profileCreated = pyqtSignal()
    backRequested = pyqtSignal()

    def __init__(self, parent=None):
        super(ProfileCreationPage, self).__init__(parent)
        self.initUI()
        self.load_styles()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.name_label = QLabel("Enter Profile Name:")
        self.name_label.setObjectName("NameLabel")
        self.layout.addWidget(self.name_label)

        self.name_edit = QLineEdit()
        self.name_edit.setObjectName("NameEdit")
        self.layout.addWidget(self.name_edit)

        self.create_button = QPushButton("Create")
        self.create_button.setObjectName("CreateButton")
        self.layout.addWidget(self.create_button)

        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("BackButton")
        self.layout.addWidget(self.back_button)

    def load_styles(self):
        try:
            with open("src/pages/profile_creation/profile_creation_page.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Error loading profile_creation_page.qss:", e)
