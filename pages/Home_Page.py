from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from gesture_utils import PREMADE_GESTURES, get_premade_gestures, is_valid_gesture


class DropdownRow(QWidget):
    def __init__(self, parent=None):
        super(DropdownRow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Create a horizontal layout for this row
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Gesture dropdown: use premade gestures from gesture_utils plus a final option "Capture Gesture"
        self.gesture_dropdown = QComboBox()
        self.gesture_dropdown.setObjectName("GestureDropdown")
        self.gesture_dropdown.addItem("Select Gesture")
        self.gesture_dropdown.addItems(PREMADE_GESTURES + ["Capture Gesture"])
        self.layout.addWidget(self.gesture_dropdown)

        # Macro dropdown
        self.macro_dropdown = QComboBox()
        self.macro_dropdown.setObjectName("MacroDropdown")
        self.macro_dropdown.addItem("Select Macro")
        self.macro_dropdown.addItems(["Open Browser", "Open Editor", "Volume Up", "Volume Down"])
        self.layout.addWidget(self.macro_dropdown)

        # Delete button to remove this row
        self.delete_button = QPushButton("-")
        self.delete_button.setFixedSize(30, 30)
        self.delete_button.setObjectName("DeleteButton")
        self.delete_button.clicked.connect(self.delete_self)
        self.layout.addWidget(self.delete_button)

    def delete_self(self):
        # Remove this row from its parent's layout and schedule it for deletion
        parent_layout = self.parentWidget().layout()
        parent_layout.removeWidget(self)
        self.deleteLater()


class HomePage(QWidget):
    def __init__(self, parent=None):
        super(HomePage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Main vertical layout for the Home page
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        # Container layout for the rows of dropdowns
        self.dropdown_container = QVBoxLayout()
        self.layout.addLayout(self.dropdown_container)

        # Add the initial row of dropdowns
        self.addDropdownRow()

        # Plus button to add a new row of dropdowns, centered at the bottom
        self.plus_button = QPushButton("+")
        self.plus_button.setFixedSize(60, 60)
        self.plus_button.setObjectName("PlusButton")
        self.plus_button.clicked.connect(self.addDropdownRow)
        self.layout.addWidget(self.plus_button, alignment=Qt.AlignCenter)

    def addDropdownRow(self):
        # Create a new row (DropdownRow widget) and add it to the container
        row = DropdownRow()
        self.dropdown_container.addWidget(row)
