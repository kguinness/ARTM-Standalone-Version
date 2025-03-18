import sys
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from pages.profile_selection.profile_selection_page import ProfileSelectionPage
from pages.profile_creation.profile_creation_page import ProfileCreationPage
from pages.profile_view.profile_page import ProfilePage
from pages.home.home_page import HomePage
from pages.gesture_capture.gesture_capture_page import GestureCapturePage
from pages.settings.settings_page import SettingsPage
from config.config import ICON_PATH

class BasicFrontendApp(QMainWindow):
    def __init__(self):
        super(BasicFrontendApp, self).__init__()
        self.current_profile = None  # Stores the selected profile name
        self.initUI()

    def initUI(self):
        # ------------------- Login Widget -------------------
        self.login_widget = QStackedWidget()
        self.profile_selection_page = ProfileSelectionPage(self)
        self.profile_selection_page.profileSelected.connect(self.on_profile_selected)
        self.login_widget.addWidget(self.profile_selection_page)

        # ------------------- Main Widget -------------------
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar with background and pink title
        self.top_bar = QWidget()
        self.top_bar.setObjectName("TopBar")
        # Set background for the top bar:
        self.top_bar.setStyleSheet("background-color: #4C4C4C;")
        top_bar_layout = QHBoxLayout(self.top_bar)
        top_bar_layout.setContentsMargins(10, 10, 10, 10)
        top_bar_layout.setSpacing(10)
        top_bar_layout.addStretch()
        self.title_button = QPushButton("ARTM")
        self.title_button.setObjectName("TitleButton")
        # Set the title text color to pink:
        self.title_button.setStyleSheet("color: #FF69B4; background: transparent; border: none; font-size: 24px; font-weight: bold;")
        self.title_button.clicked.connect(self.show_home)
        top_bar_layout.addWidget(self.title_button, alignment=Qt.AlignCenter)
        top_bar_layout.addStretch()
        main_layout.addWidget(self.top_bar)

        # Content Area: Side Bar + Content Stack
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Side Bar with background color
        self.side_bar = QWidget()
        self.side_bar.setObjectName("Sidebar")
        self.side_bar.setStyleSheet("background-color: #222222;")
        side_layout = QVBoxLayout(self.side_bar)
        side_layout.setAlignment(Qt.AlignTop)
        # Navigation buttons (except Home, which is accessed via the title)
        profile_btn = QPushButton("Profile")
        profile_btn.setObjectName("SidebarButton")
        profile_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.profile_page))
        side_layout.addWidget(profile_btn)
        gesture_btn = QPushButton("Gesture Capture")
        gesture_btn.setObjectName("SidebarButton")
        gesture_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.gesture_capture_page))
        side_layout.addWidget(gesture_btn)
        settings_btn = QPushButton("Settings")
        settings_btn.setObjectName("SidebarButton")
        settings_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.settings_page))
        side_layout.addWidget(settings_btn)
        content_layout.addWidget(self.side_bar, stretch=1)

        # Main Content Stack
        self.content_stack = QStackedWidget()
        self.home_page = HomePage(self)
        self.profile_page = ProfilePage(self)
        self.gesture_capture_page = GestureCapturePage(self)
        self.settings_page = SettingsPage(self)
        self.content_stack.addWidget(self.home_page)            # index 0: Home
        self.content_stack.addWidget(self.profile_page)           # index 1: Profile
        self.content_stack.addWidget(self.gesture_capture_page)   # index 2: Gesture Capture
        self.content_stack.addWidget(self.settings_page)          # index 3: Settings
        content_layout.addWidget(self.content_stack, stretch=4)
        main_layout.addWidget(content_widget)

        # Initially show the login widget
        self.setCentralWidget(self.login_widget)
        self.setWindowTitle("ARTM")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(900, 600)

    def on_profile_selected(self, profile_name):
        # Called when a profile is selected from the login widget.
        self.current_profile = profile_name
        # Update the profile view and home pages.
        self.profile_page.load_profile(profile_name)
        self.home_page.set_profile(profile_name)
        # Switch central widget to main_widget (which has the navigation bars).
        self.setCentralWidget(self.main_widget)
        # Show Home page by default.
        self.content_stack.setCurrentWidget(self.home_page)

    def show_home(self):
        # Called when the title button is clicked.
        self.content_stack.setCurrentWidget(self.home_page)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = BasicFrontendApp()
    window.show()
    sys.exit(app.exec_())
