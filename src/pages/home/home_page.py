from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from utils.gesture_utils import PREMADE_GESTURES


class DropdownRow(QWidget):
    def __init__(self, container_layout, parent=None):
        super(DropdownRow, self).__init__(parent)
        self.container_layout = container_layout
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.gesture_dropdown = QComboBox()
        self.gesture_dropdown.setObjectName("GestureDropdown")
        self.gesture_dropdown.addItem("Select Gesture")
        self.gesture_dropdown.addItems(PREMADE_GESTURES + ["Capture Gesture"])
        self.layout.addWidget(self.gesture_dropdown)

        self.macro_dropdown = QComboBox()
        self.macro_dropdown.setObjectName("MacroDropdown")
        self.macro_dropdown.addItem("Select Macro")
        self.macro_dropdown.addItems(["Open Browser", "Open Editor", "Volume Up", "Volume Down"])
        self.layout.addWidget(self.macro_dropdown)

        self.delete_button = QPushButton("-")
        self.delete_button.setFixedSize(30, 30)
        self.delete_button.setObjectName("DeleteButton")
        self.delete_button.clicked.connect(self.delete_self)
        self.layout.addWidget(self.delete_button)

    def delete_self(self):
        try:
            if self.container_layout is not None:
                self.container_layout.removeWidget(self)
            self.setParent(None)
            self.deleteLater()
        except Exception as e:
            print("Error deleting dropdown row:", e)


class HomePage(QWidget):
    def __init__(self, parent=None):
        super(HomePage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.dropdown_container = QVBoxLayout()
        self.layout.addLayout(self.dropdown_container)

        self.addDropdownRow()

        self.plus_button = QPushButton("+")
        self.plus_button.setFixedSize(60, 60)
        self.plus_button.setObjectName("PlusButton")
        self.plus_button.clicked.connect(self.addDropdownRow)
        self.layout.addWidget(self.plus_button, alignment=Qt.AlignCenter)

    def addDropdownRow(self):
        row = DropdownRow(self.dropdown_container)
        self.dropdown_container.addWidget(row)

    def set_profile(self, profile_name):
        print("HomePage: Profile set to", profile_name)
