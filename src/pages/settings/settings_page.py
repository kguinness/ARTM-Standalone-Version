from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super(SettingsPage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        label = QLabel("Settings Page")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

    def load_styles(self):
        try:
            with open("src/pages/settings/settings_page.qss", "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print("Error loading settings_page.qss:", e)
